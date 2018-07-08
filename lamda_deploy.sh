mkdir lunchnaste-lambda
chmod +x lunchnaste-lambda

cp setup.cfg lunchnaste-lambda
cp src/* lunchnaste-lambda

pip install -r requirements.txt -t lunchnaste-lambda

zip -r lunchnaste.zip lunchnaste-lambda

rm -rf lunchnaste-lambda