import argparse
import os
import pprint
from slackclient import SlackClient
from urllib.request import urlopen

from menu_data_helpers import CITIES, MEALS
from menu_html_parser import MenuHTMLParser
from slack_message_formatter import (
    filter_menu_during_meal,
    filter_menu_in_cities,
    format_metadata_for_slack,
)

# KW: TODO, this is specific to my key, probably shouldn't hardcode it anyways
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
    'dem-boiz': 'CBGSP0UH1',
}
PIN_CHEFS_URL = 'https://www.thepinchefs.com/menu'
SLACK_NO_CHANNEL = 'none'
SLACK_TOKEN = os.environ.get("SLACK_API_TOKEN", None)

pp = pprint.PrettyPrinter(indent=4, compact=True)

def get_raw_html():
    if os.environ.get('READ', False) == 'true':
        return urlopen(PIN_CHEFS_URL).read().decode("utf-8")
    else:
        return open('static/menu_page.html', 'r').read()

def send_to_slack(message, channel):
    sc = SlackClient(SLACK_TOKEN)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message['text'],
        as_user='true',
        attachments=message.get('attachments', None),
    )

def setup_script_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        type=string_boolean,
        default='no',
        help='debug flag to print messages to stdout')
    parser.add_argument(
        '-s',
        '--send',
        type=str,
        default=SLACK_NO_CHANNEL,
        choices=[*CHANNEL_CHOICES.keys(), SLACK_NO_CHANNEL],
        help='slack message ids where you want to send the message')

    parser.add_argument(
        '-c',
        '--cities',
        nargs='+',
        default=['SF'],
        choices=CITIES,
        help='define which cities to filter your menu search')

    parser.add_argument(
        '-m',
        '--meal',
        type=str,
        default='Lunch',
        choices=MEALS,
        help='define which meal to filter your menu search')

    return parser.parse_args()

def string_boolean(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    args = setup_script_args()

    parser = MenuHTMLParser()
    raw_html = get_raw_html()

    metadata, message = parser.feed(raw_html)

    metadata = filter_menu_in_cities(metadata, args.cities)
    metadata = filter_menu_during_meal(metadata, args.meal)
    message = format_metadata_for_slack(metadata)

    if args.debug:
        pp.pprint(message)

    if SLACK_TOKEN and args.send in CHANNEL_CHOICES.keys():
        send_to_slack(message, CHANNEL_CHOICES[args.send])

if __name__ == '__main__':
    main()