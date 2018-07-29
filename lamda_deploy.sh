#!/bin/bash

mkdir lunchnaste-lambda
chmod +x lunchnaste-lambda
if [ ! -f lunchnaste.zip ]; then
    rm lunchnaste.zip
fi

cp setup.cfg lunchnaste-lambda
cp src/* lunchnaste-lambda

pip install -r requirements.txt -t lunchnaste-lambda

# KW: deploy package needs to be in root directory, is there a better way?
cd lunchnaste-lambda
zip -r lunchnaste.zip ./*
cd ..

mv lunchnaste-lambda/lunchnaste.zip .

rm -rf lunchnaste-lambda