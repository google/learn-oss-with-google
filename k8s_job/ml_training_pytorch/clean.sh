# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

kubectl delete -f service.yaml
kubectl delete -f job.yaml --ignore-not-found=true
kubectl delete pods -l job-name=myjob --ignore-not-found=true --force --grace-period=0
kubectl wait --for=delete pod -l job-name=myjob --timeout=60s
