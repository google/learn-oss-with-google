# Distributed ML training with JAX

Here we showcase how Indexed Jobs can be used to facilitate distributed ML
training using [JAX](https://github.com/google/jax).

The focus is on integrating Indexed Jobs with the ML training code, leading to
simplifying assumptions for other aspects of the code.
For example, the code loads the entire MNIST dataset and then each worker only
filter outs its shard of data. Also, the model is very simple. Finally, the
trained version of the model isn't saved for downstream processing.

## Prepare

You can generate the Job YAML file by running the `prepare.sh` script which uses
[jinja2](https://github.com/pallets/jinja/)vto generate it based on the
template and values in the `variables.json` file.

### Image

The sample YAML file installs the required libraries on top of the
base image. In practice, you may want to build and push the image to your
repository so that it can be pulled with pre-installed dependencies.

### Requirements

The code of the Indexed Job in the current version requires GPUs in your cluster.
However, with small adjustments to the Job YAML, you will be able to run the
training on CPU. In particular, places requiring a change:
- set `local_device_count` to `1`
- remove the `spec.template.spec.containers[*].resources.limits` restriction on GPU.

## Running

To run the training execute:
```sh
./run.sh
```
This script creates a headless Service and an Indexed Job which is responsible
for creating the pods, one per host.

The training consists of multiple passes over the dataset (epochs). In each
epoch the pod distributes the dataset chunk among its local devices. After the
backward pass it averages the obtained gradients among the local devices. Next,
the model gradients are averaged across the hosts. At the final step of each
epoch the averaged gradients are used to update the model.

After the Job completes, check the output for a selected pod. It will return
output similar to this:
```
Rank 0: epoch: 8/8, batch: 468/469, batch size: 128, batch per host size: 64
Rank 0: epoch: 8/8, batch: 469/469, batch size: 96, batch per host size: 48
Rank 0: epoch 8/8, average epoch loss=0.0182
Rank 0: training completed.
```

## Clean up

In order to clean up resources (the Service, the Job and its Pods) by executing:
```
./clean.sh
```
