FROM tensorflow/tensorflow:latest-gpu-py3

RUN pip install numpy pandas scikit-learn dill dask distributed dask-ml keras
RUN mkdir /data
RUN mkdir /output
ENV PYTHONUNBUFFERED=0
COPY src /src