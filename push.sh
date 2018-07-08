#!/bin/bash

source /home/kwang/lunchnaste/bin/activate
source /home/kwang/env.sh

cd /home/kwang/lunchnaste
pip install -r requirements.txt

PYTHONPATH=. READ=true python src/send_message.py -s kwang
