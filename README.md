# Simulation of Packet Erasure Coding in a Docker-Simulated Unreliable Environment

This project aims to set up a network using Docker nodes, to simulate an unreliable network. We then evaluate the effectiveness of Packet Erasure Coding in the simulated unreliable network.

[Packet Erasure coding in an unreliable network (Poster)](poster.pdf) <br>
[Evaluation of the Effectiveness of Packet Erasure Codes in a Docker-Simulated Unreliable Network (Paper)](paper/ExtendedAbstract.pdf)


# Set up

```jsx
// Allow setup.sh to have executing permissions
chmod +x ./setup.sh // Sets up the docker environment by spinning up num_nodes derived from docker_compose.yml
chmod +x ./doSimulation.sh // Runs a simulation for multiple values of r and d
chmod +x ./doTest.sh // A single run of the simulation
```

```jsx
// to ssh into a particular node
docker ps // show all containers that are running
docker exec -it <container_id> /bin/sh // run a shell in the container

// remove docker image
docker rmi <image_id>

// show all docker images
docker images
```
