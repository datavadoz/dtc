FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get install -y wget libffi7

## Install Miniconda3
RUN TMP_DIR=$(mktemp); mkdir -p /root/miniconda3 /root/worker; \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -P ${TMP_DIR}; \
    bash ${TMP_DIR}/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -b -u -p /root/miniconda3; \
    rm -rf ${TMP_DIR}

## Install dedicated Python environment and its required packages via Miniconda3
COPY ["env.yml", "/root/worker/"]
RUN . /root/.bashrc && \
    /root/miniconda3/bin/conda init bash && \
    /root/miniconda3/bin/conda create -y -n dtc python=3.10 && \
    /root/miniconda3/bin/conda env update --name dtc --file /root/worker/env.yml

COPY ["workflow.py", "entrypoint.sh", "/root/worker/"]
ENTRYPOINT ["/bin/bash", "/root/worker/entrypoint.sh"]
