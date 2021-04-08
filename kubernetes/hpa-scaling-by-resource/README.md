# HPA: Scaling by Resource

- **Video:** [Learn Kubernetes with Google - HPA: Scaling by Resource][vid]
- **Description:** The Horizontal Pod Autoscaler (HPA) can scale your
  application up or down based on a wide variety of metrics. In this video,
  we'll cover using one of the four available metrics types: Resources or CPU
  and Memory.

**Resources:**
- [Horizontal Pod Autoscaling overview][overview]​
- [About the Horizontal Pod Autoscaler][about]
- [Horizontal Pod Autoscaler reference commands][ref]
---

## Example

- [`myapp-deployment.yaml`](./myapp-deployment.yaml) - Sample deployment
- [`myapp-autoscaler-utilization.yaml`](./myapp-autoscaler-utilization.yaml) -
  Corresponding autoscaler object using `AverageUtilization` as the scaling
  metric
- [`myapp-autoscaler-value.yaml`](./myapp-autoscaler-value.yaml) - Corresponding
  autoscaler object using `AverageValue` as the scaling metric


**NOTE:** These are reference examples; It will not autoscale. For a functional
example, see the [Horizontal Pod Autoscaler Walkthrough][hpaw].



[vid]: https://youtu.be/Na2JZfNwryM?list=PLxNYxgaZ8Rscf-XJ5VfXgbDAk1vL4xaMl
[hpaw]: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
[overview]: https://cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler
[about]: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
[ref]: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#autoscale