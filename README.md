# networksConfig
// install kind 
go install sigs.k8s.io/kind@v0.22.0

// find and export kind to path 
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