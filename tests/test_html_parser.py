import unittest
import datetime
import pprint

from menu_html_parser import MenuHTMLParser, DATE_FORMAT

pp = pprint.PrettyPrinter(indent=4, compact=True)

class TestMenuHTMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = MenuHTMLParser()
        self.raw_html = open('static/menu_page.html', 'r').read()
        self.test_date = datetime.datetime.strptime('06/22/2018', DATE_FORMAT)

    def test_feed_metadata(self):
        metadata, message = self.parser.feed(self.raw_html)

        key = ('06/22/2018', 'SF-00651', 'Breakfast')
        first_breakfast_item = metadata[key][0]

        self.assertEqual(list(metadata.keys()), list([
            ('06/22/2018', 'SF-00651', 'Breakfast'),
            ('06/22/2018', 'SF-00651', 'Lunch'),
            ('06/22/2018', 'SF-00651', 'Back 2 Basics'),
            ('06/22/2018', 'SF-00651', 'Happy Hour'),
            ('06/22/2018', 'SF-00505', 'Lunch'),
            ('06/22/2018', 'CHI-00000', 'Lunch'),
            ('06/22/2018', 'NYC-00000', 'Lunch'),
            ('06/22/2018', 'SEA-00000', 'Lunch'),
        ]))
        self.assertEqual(list(first_breakfast_item.keys()), [
            'text',
            'building',
            'meal',
            'theme',
            'is_gluten_free',
            'data'
        ])
        self.assertEqual(first_breakfast_item['text'], 'Pan d\'ajo (G D*)')
        self.assertEqual(first_breakfast_item['building'], 'SF-00651')
        self.assertEqual(first_breakfast_item['meal'], 'Breakfast')
        self.assertEqual(first_breakfast_item['theme'], 'Mexican')
        self.assertEqual(first_breakfast_item['is_gluten_free'], False)
        self.assertEqual(first_breakfast_item['data'], self.test_date)

    def test_format_error_case_covered(self):
        metadata, message = self.parser.feed(self.raw_html)

        key = ('06/22/2018', 'CHI-00000', 'Lunch')
        first_chicago_lunch_item = metadata[key][0]
        second_chicago_lunch_item = metadata[key][1]

        self.assertEqual(first_chicago_lunch_item['text'],
            'Grilled organic chicken breast with lemongrass & ginger')
        self.assertEqual(first_chicago_lunch_item['building'], 'CHI-00000')
        self.assertEqual(first_chicago_lunch_item['meal'], 'Lunch')
        self.assertEqual(first_chicago_lunch_item['theme'], 'Japanese')
        self.assertEqual(first_chicago_lunch_item['is_gluten_free'], True)
        self.assertEqual(first_chicago_lunch_item['data'], self.test_date)

if __name__ == '__main__':
    unittest.main()
