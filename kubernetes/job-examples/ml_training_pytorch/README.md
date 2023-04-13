# Distributed ML training with PyTorch

In this example, we showcase how Indexed Jobs can be used to facilitate
distributed ML training using [PyTorch](https://github.com/pytorch/pytorch).

The focus is on integrating Indexed Jobs
with the ML training code, leading to simplifying assumptions for other
aspects of the code. For example, the code loads the entire MNIST dataset and then each worker only
filter outs its shard of data. Also, the model is very simple. Finally, the
trained version of the model isn't saved for downstream processing.

## Prepare

### Job YAML

You can generate the Job YAML file by running the `prepare.sh` script which uses
[jinja2](https://github.com/pallets/jinja/)vto generate it based on the
template and values in the `variables.json` file.

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
for creating the pods. On each pod multiple processes, one per GPU device,
are started by the [torchrun](https://pytorch.org/docs/stable/elastic/run.html)
script.

The training consists of multiple passes over the dataset (epochs). In each
epoch each process trains on a chunk of data selected based on the `RANK`
env. variable. After the backward pass the model gradients are averaged over
all processes. Next, the model gradients are averaged across the hosts. At the
final step of each epoch the averaged gradients are used to update the model.

After the Job completes, check the output for a selected pod. It will return
output similar to this:
```
Rank 0: epoch: 8/8, batch: 468/469, mini-batch size: 32
Rank 1: epoch: 8/8, batch: 468/469, mini-batch size: 32
Rank 0: epoch: 8/8, batch: 469/469, mini-batch size: 24
Rank 1: epoch: 8/8, batch: 469/469, mini-batch size: 24
Rank 0: epoch 8/8, average epoch loss=0.0869
Rank 1: epoch 8/8, average epoch loss=0.0869
Rank 1: training completed.
Rank 0: training completed.
```

## Clean up

In order to clean up resources (the Service, the Job and its Pods) by executing:
```
./clean.sh
```
