# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

kubectl delete -f environment/job.yaml --ignore-not-found=true
kubectl delete pods -l job-name=environments --ignore-not-found=true --force --grace-period=0
kubectl wait --for=delete pod -l job-name=environments --timeout=60s

kubectl delete -f agent/job.yaml --ignore-not-found=true
kubectl delete pods -l job-name=agents --ignore-not-found=true --force --grace-period=0
kubectl wait --for=delete pod -l job-name=agents --timeout=60s

kubectl delete -f service.yaml --ignore-not-found=true
kubectl delete configmap environment-script
kubectl delete configmap agent-script
