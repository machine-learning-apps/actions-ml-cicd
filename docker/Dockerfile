FROM python:3.7

RUN pip install \
     numpy \
     pandas \ 
     dill \
     h5py \
     ktext \ 
     wandb

# mounting to this folder
RUN mkdir /data
# for writing artifacts
RUN mkdir /output
# For python on K8s So you can see output
ENV PYTHONUNBUFFERED=0
COPY src /src
WORKDIR data
# Scaffolding incase you want to ssh into container
RUN mkdir .ssh
RUN touch .ssh/authorized_keys

CMD scripts/run_jupyter.sh