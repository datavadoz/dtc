FROM ubuntu:22.04


RUN apt-get update -y \
    && apt-get install -y wget libffi7

## Install dedicated Python environment via Miniconda
RUN TMP_DIR=$(mktemp); mkdir -p /root/miniconda3 /root/worker; \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -P ${TMP_DIR}; \
    bash ${TMP_DIR}/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -b -u -p /root/miniconda3; \
    rm -rf ${TMP_DIR}; \
    /root/miniconda3/bin/conda init bash; \
    /root/miniconda3/bin/conda create -y -n dtc python=3.10

## Install required packages
COPY env.yml /root/worker
RUN /root/miniconda3/bin/conda env update --name dtc --file /root/worker/env.yml

