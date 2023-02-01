#!/bin/bash

source /root/miniconda3/etc/profile.d/conda.sh
conda activate dtc
prefect orion start --host 0.0.0.0
