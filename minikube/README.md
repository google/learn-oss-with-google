# local-dev-example-with-minikube


This repo demos a simple go app being deployed to a Kubernetes cluster using minikube, and demonstrates changing the code and re-deploying a new version.


## Requirements
- Clone this repo!
- Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
- Install [Docker CLI](https://minikube.sigs.k8s.io/docs/tutorials/docker_desktop_replacement/) (Docker Desktop is not required, Docker CLI is sufficent)


## Build and deploy the app to minikube for the first time!

1. Start minikube
    ```console
    minikube start
    ```

2. Point your terminal to minikube's Docker using `minikube docker-env`
    ```console
    # on Mac or Linux
    eval $(minikube docker-env)
    ```

    ```console
    # on Windows PowerShell
    & minikube docker-env | Invoke-Expression
    ```

    Tip 1: if you close your terminal you will have to re-point your docker-env.

    Tip 2: to verify that your terminal is pointing to minikube's Docker you can run `minikube status` and it will show "docker-env: in-use"

4. Build Docker image inside minikube

    ```console
    docker build -t local/devex:v1 .
    ```
4. Deploy to Kubernetes
    ```console
    kubectl apply -f deploy/k8s.yaml
    ```
5. Accees the deployed service in your browser
    ```console
    minikube service local-devex-svc
    ```
    Tip: you can try `$ minikube service list` to see all exposed serivces.


## Iterative development (how to redeploy after a code change)

1. Make a change in the code (for example bump the version in `main.go`)
2. Ensure you're still pointing to minikube's Docker using `minikube docker-env`)
3. Delete the deployment and the image
    ```console
    kubectl delete -f deploy/k8s.yaml
    docker rmi local/devex:v1
    ```
4. Rebuild the image and re-deploy to Kubernetes
    ```console
    docker build -t local/devex:v1 .
    kubectl apply -f deploy/k8s.yaml
    ```
5. Access the deployed service in your browser
    ```console
    minikube service local-devex-svc
    ```

(for faster development you can combine steps 3 and 4 the commands in one)
```
kubectl delete -f deploy/k8s.yaml;docker rmi local/devex:v1;docker build -t local/devex:v1 .;kubectl apply -f deploy/k8s.yaml
```


### Mount Files to minikube (persistent storage example)
 
- let's create a example file on our workstation (laptop) to share with our deployment in minikube
```console
mkdir -p ~/Desktop/local-devex
echo "Hello from laptop" > ~/Desktop/local-devex/hello-world.text
```

in a separate window run:
```console
 minikube mount ~/Desktop/local-devex:/data/
```
