
# Setup the environment
# Also see https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-l7-internal#gcloud_1
# and https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways#internal-gateway
kubectl apply -f gke1.yaml
kubectl apply -f ilb-gateway.yaml
kubectl apply -f bar-route.yaml
kubectl apply -f foo-route-v1.yaml

# Show the environment
kubectl apply -f foo-route-v1.yaml

# Show the environment
kubectl get services -A
kubectl get httproute -A

#bar
cat bar-route.yaml

#v1
cat foo-route-v1.yaml

export VIP1=$(kubectl get gateway ilb-gateway -o=jsonpath="{.status.addresses[0].value}" -n infra)

curl $VIP1 -H "host: foo.com"
curl $VIP1/v2 -H "host: foo.com"

curl $VIP1 -H "host: bar.com"

#v2
kubectl apply -f foo-route-v2.yaml
cat foo-route-v2.yaml

curl $VIP1 -H "host: foo.com" -H "version: v2"

#v3
kubectl apply -f foo-route-v3.yaml
cat foo-route-v3.yaml

while true; date; do curl -s ${VIP1} -H "host: foo.com" | grep metadata; sleep 1; done
