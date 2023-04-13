# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

jinja2 agent/job.yaml.j2 --format=yaml variables.json > agent/job.yaml
jinja2 environment/job.yaml.j2 --format=yaml variables.json > environment/job.yaml
