from django.test import TestCase
from putonghua.models import Character, ChinesePhrase
from putonghua.dictionary import get_phrase_pinyin, get_components_of_phrase
from putonghua.dictionary import get_toneless_pinyin_components
from .base import test_resource_file

from putonghua.forms import ChinesePhraseForm
from putonghua.forms import VALID_PINYIN_ERROR, CAPITALIZED_PINYIN_ERROR

DEFAULT_REQUIRED_ERROR = "This field is required."

class ChinesePhraseFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ChinesePhraseForm()
        self.assertIn('name="pinyin"', form.as_p())
        self.assertIn('name="english"', form.as_p())


    def test_form_validation_for_pinyin_without_tones(self):
        form = ChinesePhraseForm(data={'pinyin': 'lun2 yi3',
                                       'english': 'wheelchair',
                                       'is_name': False})
        self.assertTrue(form.is_valid())

        form = ChinesePhraseForm(data={'pinyin': 'lun yi3',
                                       'english': 'wheelchair',
                                       'is_name': False})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['pinyin'], [VALID_PINYIN_ERROR])

        form = ChinesePhraseForm(data={'pinyin': 'Lun2 yi3',
                                       'english': 'wheelchair',
                                       'is_name': False})
        self.assertFalse(form.is_valid())
        self.assertIn([CAPITALIZED_PINYIN_ERROR], form.errors.values())

        form = ChinesePhraseForm(data={'pinyin': '',
                                       'english': 'wheelchair',
                                       'is_name': False})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['pinyin'], [DEFAULT_REQUIRED_ERROR])



                                 
