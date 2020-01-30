FROM jupyter/datascience-notebook

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
# Install Python packages

RUN pip --no-cache-dir install --upgrade \
    fastscript \
    jupyter_client \
    ipykernel 

RUN mkdir mlops
WORKDIR /home/jovyan/mlops

