# Learn OSS with Google

Welcome! This repo serves as the home to snippets and examples from the
Learn Open Source with Google Video Series! A series of short videos from
Google Experts going over a wide variety of topics.

- [Kubernetes](./kubernetes) ([Playlist][lkwg])
  - [Intro to Horizontal Pod Autoscaler (HPA)](./kubernetes/hpa-introduction)
  - [HPA: Scaling by Resource](./kubernetes/hpa-scaling-by-resource)
  - [Gateway API: Key concepts](./kubernetes/gateway-concepts/)
  - [Gateway API: HTTP Routing](./kubernetes/http-routing/)

[lkwg]: https://youtube.com/playlist?list=PLxNYxgaZ8Rscf-XJ5VfXgbDAk1vL4xaMl

## K8s Job usage examples

This repo also showcases the use of
[Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
to perform various tasks. The examples focus on the Job-code integration, so
some aspects of the code are simplified.

Examples:
- [Distributed ML training with JAX](./k8s_job/ml_training_jax/)
- [Distributed ML training with PyTorch](./k8s_job/ml_training_pytorch/)
- [Agent-environment simulations](./k8s_job/catch_game/)
