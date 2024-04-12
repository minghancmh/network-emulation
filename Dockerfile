# Dockerfile for source node
FROM kindest/node:v1.21.14

# Set working directory
WORKDIR /app

RUN apt update && apt-get install python3-pip -y

# Copy source node script and any dependencies
COPY node.py /app/


# Install dependencies
RUN pip install netifaces

# Run the source node script 
ENTRYPOINT ["python3", "-u", "node.py", "--listen"]
# ENTRYPOINT ["/app/entrypoint.sh"]



#docker run -it --entrypoint=/bin/bash node_image
