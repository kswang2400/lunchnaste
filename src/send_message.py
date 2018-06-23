import argparse
import os
import pprint
from slackclient import SlackClient
from urllib.request import urlopen

from menu_html_parser import MenuTextParser

SLACK_NO_CHANNEL = 'none'
CHANNEL_CHOICES = [SLACK_NO_CHANNEL, 'all', 'kwang', 'seo-young']
KWANG_SLACK_ID = 'D751KUUUA'
PIN_CHEFS_URL = 'https://www.thepinchefs.com/menu'
SEO_YOUNG_SLACK_ID = 'G5BT1KEP8'
SLACK_TOKEN= os.environ["SLACK_API_TOKEN"]

pp = pprint.PrettyPrinter(indent=4, compact=True)

def create_message():
    # raw_html = urlopen(PIN_CHEFS_URL).read().decode("utf-8")

    raw_html = open('static/menu_page.html', 'r').read()

    parser = MenuTextParser()
    output = parser.feed(raw_html)

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c',
        '--channel',
        type=str,
        default=SLACK_NO_CHANNEL,
        choices=CHANNEL_CHOICES,
        help='slack message ids where you want to send the message')

    args = parser.parse_args()

    metadata, message = create_message()

    pp.pprint(metadata)
    print(message)

    if args.channel is not SLACK_NO_CHANNEL:
        sc = SlackClient(SLACK_TOKEN)
        sc.api_call(
            "chat.postMessage",
            channel=KWANG_SLACK_ID,
            text=message,
        )
