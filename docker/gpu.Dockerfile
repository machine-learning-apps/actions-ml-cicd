FROM tensorflow/tensorflow:2.0.0-gpu-py3

RUN pip install pandas wandb h5py
RUN mkdir /data
RUN mkdir /output

# Scaffolding incase you want to ssh into container
RUN mkdir ~/.ssh
RUN touch ~/.ssh/authorized_keys

ENV PYTHONUNBUFFERED=0
COPY src /src