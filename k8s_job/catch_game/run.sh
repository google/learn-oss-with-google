# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

kubectl create -f service.yaml

kubectl create configmap environment-script --from-file=catch_environment.py=environment/catch_environment.py --dry-run=client -o yaml | kubectl apply -f -
kubectl create configmap agent-script --from-file=catch_ai_agent.py=agent/catch_ai_agent.py --dry-run=client -o yaml | kubectl apply -f -

kubectl create -f environment/job.yaml
kubectl create -f agent/job.yaml
