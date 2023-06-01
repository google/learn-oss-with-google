FROM golang:alpine

# Set the Current Working Directory inside the container
WORKDIR $GOPATH/src/github.com/medyagh/local-dev-example-with-minikube/

# Copy everything from the current directory to the PWD (Present Working Directory) inside the container
COPY . .

# Install the package
RUN go install -v ./...

# This container exposes port 8080 to the outside world
EXPOSE 8080

# Run the executable
CMD ["local-dev-example-with-minikube"]