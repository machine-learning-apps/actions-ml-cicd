FROM python:3.7

RUN pip install dask[dataframe] --upgrade
RUN pip install ktext \
     numpy \
     pandas \ 
     scikit-learn \
     dill \
     ktext \ 
     tensorflow \
     distributed \
     dask-ml \
     ipython \
     jupyterlab

RUN apt-get update && apt-get install htop -y
RUN apt-get install openssh-server -y
RUN apt-get install vim -y

# mounting to this folder
RUN mkdir /data
# for writing artifacts
RUN mkdir /output
# For python on K8s So you can see output
ENV PYTHONUNBUFFERED=0
COPY src /src
WORKDIR data
RUN mkdir .ssh
RUN touch .ssh/authorized_keys
CMD scripts/run_jupyter.sh