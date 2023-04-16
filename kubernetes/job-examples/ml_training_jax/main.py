# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Tuple
import sys, logging
import jax
import jax.lax
import jax.numpy as jnp

import flax.linen as nn
import optax

import tensorflow as tf
import tensorflow_datasets as tfds

# Set up logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s')
handler.setFormatter(formatter)
root.handlers.clear()
root.addHandler(handler)

NUM_EPOCHS = 8   # number of training passes over the training dataset
BATCH_SIZE = 128 # dataset batch size; each batch gets evenly distributed across hosts and local devices per host

# Define the neural network model
class MLP(nn.Module):

    @nn.compact
    def __call__(self, x):
        x = x.reshape((x.shape[0], -1))
        x = nn.Dense(256)(x)
        x = nn.relu(x)
        x = nn.Dense(128)(x)
        x = nn.relu(x)
        x = nn.Dense(10)(x)
        return x

model = MLP()
optimizer = optax.adam(learning_rate=0.001)

# Define the training functions
def cross_entropy_loss(logits: jnp.ndarray, labels: jnp.ndarray) -> jnp.ndarray:
    one_hot_labels = jax.nn.one_hot(labels, logits.shape[-1])
    return -jnp.mean(jnp.sum(one_hot_labels * jax.nn.log_softmax(logits), axis=-1))

# Computes the loss for the given model using the provided inputs and labels.
def loss_fn(params: Any, inputs: jnp.ndarray, labels: jnp.ndarray) -> jnp.ndarray:
    logits = model.apply({'params': params}, inputs)
    return cross_entropy_loss(logits, labels)

# Splits the first axis of `arr` evenly across the number of local devices.
def split(arr: jnp.ndarray) -> jnp.ndarray:
    n_local_devices = jax.local_device_count()
    return arr.reshape(n_local_devices, arr.shape[0] // n_local_devices, *arr.shape[1:])

# Computes gradients on the given mini-batch, then averages gradients across devices and updates the model parameters
# jit annotation is optional as the function is only used in the pmap context
@jax.jit
def update_fun(params: Any, optimizer_state: Any, inputs: jnp.ndarray, labels: jnp.ndarray) -> Any:
    loss, grads = jax.value_and_grad(loss_fn)(params, inputs, labels)
    avg_loss, avg_grads = jax.lax.pmean((loss, grads), axis_name='i')
    updates, optimizer_state = optimizer.update(avg_grads, optimizer_state)
    params = optax.apply_updates(params, updates)
    return params, optimizer_state, avg_loss

# Load the shard of the MNIST dataset corresponding to the rank
def load_mnist_shard(split: str, rank: int, size: int) -> Tuple[tf.data.Dataset, tfds.core.DatasetInfo]:
    ds, ds_info = tfds.load('mnist', split=split, with_info=True, as_supervised=True)
    ds_shard = ds.shard(size, rank)
    ds_shard = ds_shard.map(lambda image, label: (tf.image.convert_image_dtype(image, tf.float32), tf.cast(label, tf.int32)))
    return ds_shard, ds_info

# Main function for running the training
def run(rank, world_size):
    logging.info(f"Rank {rank}: world_size (hosts count): {world_size}")
    logging.info(f"Rank {rank}: has {jax.local_device_count()} local devices: {jax.local_devices()}")
    logging.info(f"Rank {rank}: sees {jax.device_count()} devices: {jax.devices()}")

    train_ds_shard, train_ds_info = load_mnist_shard('train', rank, world_size)
    train_ds_shard_in_batches = train_ds_shard.batch(BATCH_SIZE // world_size)

    # Initialize random number generation
    rng = jax.random.PRNGKey(0)
    rng, init_rng = jax.random.split(rng)

    input_shape = (1, *train_ds_info.features['image'].shape)
    params = model.init(init_rng, jnp.ones(input_shape, jnp.float32))['params']

    # Initialize the optimizer
    optimizer_state = optimizer.init(params)

    # Replicate parameters across the local devices on each host
    replicated_params = jax.tree_util.tree_map(lambda x: jnp.array([x] * jax.local_device_count()), params)
    replicated_optimizer_state = jax.tree_util.tree_map(lambda x: jnp.array([x] * jax.local_device_count()), optimizer_state)

    # Train the model
    for epoch in range(NUM_EPOCHS):
        avg_epoch_loss = 0
        for batch_num, batch in enumerate(train_ds_shard_in_batches):
            batch_inputs_np, batch_labels_np = tfds.as_numpy(batch)

            split_inputs = split(jnp.array(batch_inputs_np))
            split_labels = split(jnp.array(batch_labels_np))

            replicated_params, replicated_optimizer_state, replicated_avg_loss = jax.pmap(update_fun, axis_name="i")(replicated_params, replicated_optimizer_state, split_inputs, split_labels)

            avg_epoch_loss += replicated_avg_loss[0]
            logging.info(f"Rank {rank}: epoch: {epoch+1}/{NUM_EPOCHS}, batch: {batch_num+1}/{len(train_ds_shard_in_batches)}, batch size: {batch_inputs_np.shape[0] * world_size}, batch per host size: {batch_inputs_np.shape[0]}")

        avg_epoch_loss /= len(train_ds_shard_in_batches)
        logging.info(f"Rank {rank}: epoch {epoch+1}/{NUM_EPOCHS}, average epoch loss={avg_epoch_loss:.4f}")

    logging.info(f"Rank {rank}: training completed.")

if __name__ == "__main__":
    """ Initialize the distributed environment. """
    rank = int(sys.argv[1])
    world_size = int(sys.argv[2])
    coordinator_address = sys.argv[3]
    logging.info(f"Rank: {rank}: initializing distributed environment, world size: {world_size}, coordinator address: {coordinator_address}")
    jax.distributed.initialize(
        coordinator_address=coordinator_address,
        num_processes=world_size,
        process_id=rank)
    run(rank, world_size)
