# Agent-Environment simulations

This example builds on top and adapts the code of the "Catch game" example in
the [dm_env_rpc](https://github.com/deepmind/dm_env_rpc) library.

Here, we showcase how Indexed Jobs can be used to perform replicated
agent-environment simulations to account for variations in both agent and
environment. The focus is on integrating Indexed Jobs with the code operating
the replicated agents and environments, leading to certain simplifications.
For example, the simulation results (rewards and actions) are only displayed in
the console, and are not used by the machine learning process of the agent.

## Prepare

You can generate the Job YAML files for both agent and environments by running
the `prepare.sh` script which uses [jinja2](https://github.com/pallets/jinja/)
to generate them based on the templates and values in the `variables.json` file.

### Image

The sample YAML file installs the required libraries on top of the
base image. In practice, you may want to build and push the image to your
repository so that it can be pulled with pre-installed dependencies.

## Running

To run the simulation execute:
```sh
./run.sh
```
This script creates a headless Service and a pair of Indexed Jobs. The job
named `agents` is used to start a set of pods representing agents. Also, the job
named `environments` is used to create replicas of the environments.

After completed execution you can check that all pods are completed, by running:
```sh
kubectl get pods
```
It will return output similar to this:
```
NAME                   READY   STATUS      RESTARTS   AGE
agents-0-lnvrj         0/1     Completed   0          8s
agents-1-thkpk         0/1     Completed   0          8s
agents-2-9hvpw         0/1     Completed   0          8s
agents-3-dnjrb         0/1     Completed   0          8s
agents-4-5r9v6         0/1     Completed   0          8s
environments-0-b4jtq   0/1     Completed   0          9s
environments-1-4g2k8   0/1     Completed   0          9s
environments-2-87bbp   0/1     Completed   0          9s
environments-3-9kjbj   0/1     Completed   0          9s
environments-4-hnxxq   0/1     Completed   0          9s
```

You can check the reward of a selected agent by running:
```sh
kubectl logs agents-0-lnvrj
```
The last line will contain the reward value in a format similar to this:
```
total_reward 10.0
```

## Clean up

In order to clean up resources (the Service and the Jobs) created by the
simulation execute:
```
./clean.sh
```
