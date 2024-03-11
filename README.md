# networksConfig
```jsx
// install kind 
go install sigs.k8s.io/kind@v0.22.0

// find and export kind fo path 
// first run 
go env GOPATH
// go to that variable, find the folder that contains kind
pwd
// copy the output (ie /Users/minghanchan/go/bin)
//depending on which shell you use, do, for zshrc
vim ~/.zshrc 

//append to the back of .zshrc
export PATH=/Users/minghanchan/go/bin:$PATH

// to ssh into a particular node
docker ps // show all containers that are running
docker exec -it <container_id> /bin/sh // run a shell in the container
```

```jsx

// Creating a new cluster
kind create cluster --name k8s-playground --config kind-config.yaml

// Deleting the cluster
kind delete cluster --name k8s-playground

// show all kind clusters
kind get clusters

// show all nodes in a cluster
kubectl get nodes

// get cluster info
kubectl cluster-info --context kind-k8s-playground

// see all active connections
ss -tuln

// see incoming packets
watch -d "cat /proc/net/snmp | grep -w Udp" 

// building a new docker image from Dockerfile
docker build -t my-custom-kindest-node .

// remove docker image
docker rmi <image_id>

// show all docker images
docker images
```
