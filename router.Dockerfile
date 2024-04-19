# Dockerfile for source node
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

RUN apt update && apt-get install python3-pip -y

# Copy source node script and any dependencies
COPY ecgen /app/


# Install dependencies
RUN conda env create -f environment.yml


# # Activate Conda environment and set default shell
# RUN echo "conda activate netsim" >> ~/.bashrc
# ENV SHELL /bin/bash

# Activate Conda environment and set default shell
SHELL ["conda", "run", "-n", "netsim", "/bin/bash", "-c"]


# Run the source node script
RUN pip install zfec 
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "netsim", "python3", "-u", "node.py", "--nodeType", "router"]




#docker run -it --entrypoint=/bin/bash networksconfig-node



