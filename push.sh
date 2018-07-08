#!/bin/bash

source /home/kwang/lunchnaste/bin/activate

cd /home/kwang/lunchnaste
pip install -r requirements.txt

PYTHONPATH=. READ=true python src/send_message.py -s kwang
