import logging
import os

from send_message import read_from_blog, send_to_slack

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    event_args = parse_lambda_event(event)

    response = send_to_slack(
        read_from_blog(event_args['cities'], event_args['meal']),
        event_args['channel_id'],
        os.environ.get('KW_{crew}'.format(crew=event_args['crew']))
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response),
    }

def parse_lambda_event(event):
    default_args = {
        'cities': ['SF'],
        'crew': 'PIN',
        'recipient': 'seo-young',
        'meal': 'Lunch',
    }

    event_args = event['queryStringParameters'].copy()
    event_args.update(default_args)

    return event_args