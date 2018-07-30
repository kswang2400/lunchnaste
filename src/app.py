import json
import logging
import os
import time

from send_message import read_from_blog, send_to_slack

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEFAULT_MEAL = 'Lunch'
DEFAULT_CITY = 'SF'

def lambda_handler(event, context):
    logger.info(event)
    logger.info('request text passed in: {text}'.format(text=event['queryStringParameters']['text']))

    event_args = parse_lambda_event(event)

    response = send_to_slack(
        read_from_blog(event_args['cities'], event_args['meal']),
        event_args['channel_id'],
        os.environ.get('KW_{crew}'.format(crew=event_args['crew']))
    )

    if response['ok']:
        statusCode = 200
        message = 'lunchnaste success!'
    else:
        statusCode = 500
        message = response['error']

    logger.info(response)

    return {
        'statusCode': statusCode,
        'body': message,
    }

def parse_lambda_event(event):
    default_args = {
        'cities': ['SF'],
        'crew': 'PIN',
        'recipient': 'seo-young',
        'meal': DEFAULT_MEAL,
    }

    event_args = event['queryStringParameters'].copy()

    city, meal = parse_event_query_text(event_args['text'])

    default_args['cities'] = [city]
    default_args['meal'] = meal

    event_args.update(default_args)

    return event_args

def parse_event_query_text(text):
    args = text.split(' ')

    if len(args) > 1:
        city = parse_city_text(args[0])
        meal = parse_meal_text(args[1])
    else:
        city = parse_city_text(args[0])
        meal = DEFAULT_MEAL

    return (city, meal)

def parse_city_text(string):
    VALID_CITY_STRINGS = {
        'SF': ['sf', 'san-francisco'],
        'CHI': ['chi', 'chicago'],
        'NYC': ['nyc', 'new-york'],
        'SEA': ['sea', 'seattle'],
    }

    for city, valid_strings in VALID_CITY_STRINGS.items():
        if string.lower() in valid_strings:
            return city

    return DEFAULT_CITY

def parse_meal_text(string):
    VALID_MEAL_STRINGS = {
        'Breakfast': ['breakfast', 'bfast', 'desayuno'],
        'Lunch': ['lunch', 'almuerzo'],
        'Dinner': ['dinner', 'supper', 'cena'],
    }

    for meal, valid_strings in VALID_MEAL_STRINGS.items():
        if string.lower() in valid_strings:
            return meal

    return DEFAULT_MEAL
