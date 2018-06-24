import datetime
from html.parser import HTMLParser

from src.menu_data_helpers import (
    MEALS,
    is_empty,
    is_gluten_free,
    menu_section_name,
    fix_format_error,
    parse_city_metadata,
    parse_meal_metadata,
)

GET_DATE_FLAG = '~get date~'
DATE_FORMAT = '%m/%d/%Y'

class MenuHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = ''
        self.menu_section = 0
        self.data = {}
        self.date = False
        self.building = None
        self.meal = None
        self.theme = None

        # KW: menu is inconsistent between SF and non-SF offices
        self.format_error_flag = False

        # <font>Lunch 11:45am - 1:30 pm - Vietnamese</font>

        # <font>
        #     Lunch-&nbsp;
        #     <span>11:45 am - 1:30 pm - DIY Pho Noodle Bar&nbsp;</span>
        # </font>

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[1] in ['blog-content', 'blog-comments-bottom']:
                self.menu_section += 1
            if attr[1] == 'date-text':
                self.date = GET_DATE_FLAG

        return

    def handle_data(self, data):
        if is_empty(data):
            return

        if self.date == GET_DATE_FLAG:
            self.date = datetime.datetime.strptime(data.strip(), DATE_FORMAT)
            return

        if self.menu_section == 1:
            self._collect_data(data)

        return

    def feed(self, data):
        super().feed(data)
        return (self.data, self.output)

    def _append_to_output_string(self, data):
        warning = '' if is_gluten_free(data) else ':warning: '
        spacing = {
            'city': '\n',
            'meals': '\t',
            'menu_item': '\t\t',
        }[menu_section_name(data)]

        self.output += '{spacing}{warning}{data}\n'.format(
            spacing=spacing,
            warning=warning,
            data=data)

        return

    def _build_menu_metadata_key(self):
        key = (self.date.strftime(DATE_FORMAT), self.building, self.meal)
        if key not in self.data:
            self.data[key] = []

        return key

    def _collect_data(self, data):
        self._collect_metadata(data)
        self._append_to_output_string(data)

        return

    def _collect_metadata(self, data):
        is_header = self._parse_and_set_header_metadata(data)

        if not is_header:
            menu_item_data = self._format_menu_item_data(data)
            self._store_menu_item_data(menu_item_data)

        return

    def _format_menu_item_data(self, data):
        return {
            'text': data,
            'building': self.building,
            'meal': self.meal,
            'theme': self.theme,
            'is_gluten_free': is_gluten_free(data),
            'data': self.date,
        }

    def _parse_and_set_header_metadata(self, data):
        if self.format_error_flag:
            self.theme = fix_format_error(data)
            self.format_error_flag = False
            return True

        if is_empty(data):
            return True

        city_metadata = parse_city_metadata(data)
        if city_metadata:
            self.building = city_metadata
            return True

        meal_metadata = parse_meal_metadata(data)
        if meal_metadata:
            self.meal, self.theme = meal_metadata
            if self.theme in ['\xa0', '']:
                self.format_error_flag = True
                self.theme = None
            return True

        return False

    def _store_menu_item_data(self, menu_item_data):
        key = self._build_menu_metadata_key()
        self.data[key].append(menu_item_data)

        return
