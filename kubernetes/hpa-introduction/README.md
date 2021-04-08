# Intro to Horizontal Pod Autoscaler (HPA)

**Video:** [Learn Kubernetes with Google - Intro to Horizontal Pod Autoscaler (HPA)][vid]

**Description:** The Horizontal Pod Autoscaler (HPA) is a Kubernetes
  primitive that enables you to dynamically scale your application (pods) up or
  down based on your workloads resource utilization such as CPU or Memory, or
  other potential metrics related to your app.

**Resources:**
- [Horizontal Pod Autoscaling overview][overview]​
- [About the Horizontal Pod Autoscaler][about]
- [Horizontal Pod Autoscaler reference commands][ref]

---

## Example

- [`nginx-deployment.yaml`](./nginx-deployment.yaml) - Sample deployment
- [`nginx-autoscaler.yaml`](./nginx-autoscaler.yaml) - Corresponding autoscaler object

**NOTE:** These are reference examples; it will not autoscale. For a functional
example, see the [Horizontal Pod Autoscaler Walkthrough][hpaw].



[vid]: https://youtu.be/nRKKYtPWYGs?list=PLxNYxgaZ8Rscf-XJ5VfXgbDAk1vL4xaMl
[hpaw]: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
[overview]: https://cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler
[about]: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
[ref]: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#autoscale