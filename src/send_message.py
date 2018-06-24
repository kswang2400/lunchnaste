import argparse
import os
import pprint
from slackclient import SlackClient
from urllib.request import urlopen

from menu_html_parser import MenuHTMLParser

CHANNEL_CHOICES = {
    # seo-young
    'chidinma': 'D7A466R62',
    'kwang': 'D751KUUUA',
    'seo-young': 'G5BT1KEP8',

    # klayy-lmao
    'eric-huang': 'D8R13MBMM',
    'eric-pham': 'DAXNA4Q5B',
    'evan': 'D3B1Q1YNT',
    'kevin': 'D39KFCW7J',
    'ollie': 'D3A8V5K3M',
}
PIN_CHEFS_URL = 'https://www.thepinchefs.com/menu'
SLACK_NO_CHANNEL = 'none'
SLACK_TOKEN= os.environ.get("SLACK_API_TOKEN", None)

pp = pprint.PrettyPrinter(indent=4, compact=True)

def get_raw_html():
    if os.environ.get('READ', False) == 'true':
        return urlopen(PIN_CHEFS_URL).read().decode("utf-8")
    else:
        return open('static/menu_page.html', 'r').read()

def string_boolean(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        type=string_boolean,
        default='yes',
        help='slack message ids where you want to send the message')
    parser.add_argument(
        '-c',
        '--channel',
        type=str,
        default=SLACK_NO_CHANNEL,
        choices=[*CHANNEL_CHOICES.keys(), SLACK_NO_CHANNEL],
        help='slack message ids where you want to send the message')
    args = parser.parse_args()

    parser = MenuHTMLParser()
    raw_html = get_raw_html()
    metadata, message = parser.feed(raw_html)

    if args.debug:
        pp.pprint(metadata)
        print(message)

    if SLACK_TOKEN and args.channel in CHANNEL_CHOICES.keys():
        sc = SlackClient(SLACK_TOKEN)
        sc.api_call(
            "chat.postMessage",
            channel=CHANNEL_CHOICES[args.channel],
            text=message,
        )
