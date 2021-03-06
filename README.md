# lunchnaste bot

### usage

```
echo "export SLACK_API_TOKEN='<your-slack-api-token>'" >> env.sh
source env.sh
PYTHONPATH=. [READ=true] python src/send_message.py [--debug=false] [-s kwang]
```

- READ: make network call to pinchefs site or use static test html
- debug: prints debug to stdout
- channel: sends to slack channel

### setup

```
mkvirtualenv --python=`which python3` lunchnaste
workon lunchnaste

# devapp
scp env.sh kwang@dev-kwang.ec2.pin220.com:env.sh

virtualenv --python=`which python3` lunchnaste
source /home/kwang/lunchnaste/bin/activate
source ~/env.sh
```

# lambda deploy

```
source lambda_deploy.sh
upload lunchnaste.zip to aws lambda
```

### tests

- `PYTHONPATH=src pytest`

### roadmap

- [x] parse menu data from pincuisine blog
- [x] slack slash command integration
- [ ] set up voting bot to figure out which building to crew up
- [ ] support sending to multiple channels/users
- [x] include other offices (for when we can afford to fly to nyc for lunch)

