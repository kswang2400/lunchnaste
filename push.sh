#!/bin/bash


DEBUG=$1
CREW=$2
RECIPIENT=$3
MEAL=$4

DATE=`date '+%Y-%m-%d %H:%M:%S'`
TOKEN_NAME=KW_$CREW

echo "[$DATE] sending $MEAL menu to $RECIPIENT"
source /home/kwang/lunchnaste/bin/activate
source /home/kwang/env.sh

cd /home/kwang/lunchnaste
pip install -r requirements.txt --quiet
export SLACK_API_TOKEN=${!TOKEN_NAME}

PYTHONPATH=. READ=true python src/send_message.py -d $DEBUG -s $RECIPIENT -m $MEAL

echo "[$DATE] success"
