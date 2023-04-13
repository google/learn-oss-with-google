# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

kubectl create -f service.yaml
kubectl create configmap script --from-file=main.py=main.py --dry-run=client -o yaml | kubectl apply -f -
kubectl create -f job.yaml
