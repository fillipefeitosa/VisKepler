FROM continuumio/miniconda3

LABEL maintainer="fillfeitosa@gmail.com"

# Mamba makes the environment faster
RUN conda install -c conda-forge mamba libarchive -y

# Set the working directory in docker
WORKDIR /app

# Copy everything into the container at /app and install dependencies
COPY . /app/

# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH

# Create the environment
RUN mamba env create -f environment.yml

# Expose the port the app runs on
EXPOSE 8050

# Command to run on container start
CMD ["bash", "-c", "source activate $(head -1 /app/environment.yml | cut -d' ' -f2) && uvicorn --host 0.0.0.0 --port 8050 --reload main:app"]