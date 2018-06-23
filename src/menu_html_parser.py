import datetime
from html.parser import HTMLParser

MEALS = ('Breakfast', 'Lunch', 'Dinner', 'Back 2 Basics', 'Happy Hour',)
GET_DATE_FLAG = '~get date~'
DATE_FORMAT = '%m/%d/%Y'

def empty_data(data):
    return ''.join(data.split()) == '' or data == '\u200b'

def is_menu_header(data):
    for meal in (*MEALS, 'SF'):
        if data.startswith(meal):
            return True
    return False

def menu_item_has_gluten(text):
    if '(' not in text:
        return False

    return 'G' in text.split('(')[1].split(')')[0]

class MenuTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = ''
        self.menu_section = 0

        # KW: v2 iteration stores parsed data for analysis
        # requires parsing HTML in order though
        self.data = {}
        self.date = False
        self.building = None
        self.meal = None
        self.theme = None

    def parse_and_set_metadata(self, data):
        if empty_data(data):
            return False

        if data.startswith('SF'):
            self.building = '{city}-{address}'.format(
                city=data[:2],
                address=data[2:])
            return

        for meal in MEALS:
            if data.startswith(meal):
                self.meal = meal
                self.theme = data.split(' - ')[-1]
                return

        return not is_menu_header(data)

    def collect_data(self, data):
        self.collect_metadata(data)

        warning = ':warning: ' if menu_item_has_gluten(data) else ''
        spacing = '\n' if is_menu_header(data) else '\t'

        self.output += '{spacing}{warning}{data}\n'.format(
            spacing=spacing,
            warning=warning,
            data=data)

        return

    def collect_metadata(self, data):
        is_menu_item = self.parse_and_set_metadata(data)

        if is_menu_item:
            menu_item_data = {
                'text': data,
                'building': self.building,
                'meal': self.meal,
                'theme': self.theme,
                'has_gluten': menu_item_has_gluten(data),
                'data': self.date,
            }

            key = (self.date.strftime(DATE_FORMAT), self.building, self.meal)
            if key in self.data:
                self.data[key].append(menu_item_data)
            else:
                self.data[key] = [menu_item_data]

        return

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[1] in ['blog-content', 'blog-comments-bottom']:
                self.menu_section += 1
            if attr[1] == 'date-text':
                self.date = GET_DATE_FLAG

        return

    def handle_data(self, data):
        if empty_data(data):
            return

        if self.date == GET_DATE_FLAG:
            self.date = datetime.datetime.strptime(data.strip(), DATE_FORMAT)
            return

        if data == 'CHI':
            self.menu_section += 1

        if self.menu_section == 1:
            self.collect_data(data)

        return

    def feed(self, data):
        super().feed(data)
        return (self.data, self.output)
