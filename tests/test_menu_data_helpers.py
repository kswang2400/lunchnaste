import unittest
from src.menu_data_helpers import check_allergen_key


class AllergensTest(unittest.TestCase):
    def test_no_allergens(self):
        allergens = check_allergen_key('*jk**hgNjsGhSgfEk')
        self.assertFalse(allergens.is_vegetarian)
        self.assertFalse(allergens.is_vegan)
        self.assertTrue(allergens.is_gluten_free)
        self.assertFalse(allergens.is_made_with_dairy)
        self.assertFalse(allergens.is_made_with_nuts)
        self.assertFalse(allergens.is_made_with_eggs)
        self.assertFalse(allergens.is_made_with_soy)

    def test_vegeterian(self):
        self.assertTrue(check_allergen_key('gkgh(*)sjfkbfkg').is_vegetarian)

    def test_vegan(self):
        self.assertTrue(check_allergen_key('hsgbksfg(**)sjlfjgks').is_vegan)

    def test_vegan_and_vegeterarian(self):
        allergens = check_allergen_key('asgas(*,**)ahkfbasf')
        self.assertTrue(allergens.is_vegetarian)
        self.assertTrue(allergens.is_vegan)

    def test_gluten(self):
        self.assertFalse(check_allergen_key('jsaf(G)aksfkajf').is_gluten_free)

    def dairy(self):
        self.assertTrue(check_allergen_key('fk(D)kjhagkgk').is_made_with_dairy)

    def nuts(self):
        self.assertTrue(check_allergen_key('kjga(N)jnfnsf').is_made_with_nuts)

    def eggs(self):
        self.assertTrue(check_allergen_key('khss(E)hbsjhfd').is_made_with_eggs)

    def soy(self):
        self.assertTrue(check_allergen_key('hjaf(S)hjgfjsf').is_made_with_soy)
