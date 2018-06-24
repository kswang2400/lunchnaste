import unittest
import datetime

from src.menu_html_parser import MenuHTMLParser, DATE_FORMAT

class TestMenuHTMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = MenuHTMLParser()
        self.raw_html = open('static/menu_page.html', 'r').read()

    def test_feed(self):
        metadata, message = self.parser.feed(self.raw_html)
        first_breakfast_item = metadata[('06/22/2018', 'SF-651', 'Breakfast')][0]

        self.assertEqual(list(metadata.keys()), list([
            ('06/22/2018', 'SF-651', 'Breakfast'),
            ('06/22/2018', 'SF-651', 'Lunch'),
            ('06/22/2018', 'SF-651', 'Back 2 Basics'),
            ('06/22/2018', 'SF-651', 'Happy Hour'),
            ('06/22/2018', 'SF-505', 'Lunch')
        ]))
        self.assertEqual(list(first_breakfast_item.keys()), [
            'text',
            'building',
            'meal',
            'theme',
            'has_gluten',
            'data'
        ])
        self.assertEqual(first_breakfast_item['text'], 'Pan d\'ajo (G D*)')
        self.assertEqual(first_breakfast_item['building'], 'SF-651')
        self.assertEqual(first_breakfast_item['meal'], 'Breakfast')
        self.assertEqual(first_breakfast_item['theme'], 'Mexican')
        self.assertEqual(first_breakfast_item['has_gluten'], True)
        self.assertEqual(first_breakfast_item['data'], datetime.datetime.strptime('06/22/2018', DATE_FORMAT))

if __name__ == '__main__':
    unittest.main()
