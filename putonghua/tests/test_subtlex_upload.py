from .base import test_resource_file
from django.test import TestCase
from django.db.models import Sum
import putonghua.subtlex as subtlex
from putonghua.models import SubtlexCharData, SubtlexWordData
from putonghua.models import Character, ChinesePhrase, ChineseWord


class SubtlexUploadTest(TestCase):
    fixtures = ['fifteen_chars_phrases.json']
    CHAR_SAMPLE_SET_SIZE = 44069143
    NI_SAMPLE_COUNT = 1444831
    
    WORD_SAMPLE_SET_SIZE  = 27441642
    YINWEI_SAMPLE_COUNT   = 59823
    ZAI_WORD_SAMPLE_COUNT = 429766
    
    def test_upload_char_data_and_compute_scores(self):
        subtlex.upload_subtlex_char_data(test_resource_file('subtlex_char_sample_set_1.csv'))
        self.assertEqual(2058980, SubtlexCharData.objects.get(simplified='我').count)
        self.assertEqual(self.NI_SAMPLE_COUNT, SubtlexCharData.objects.get(simplified='你').count)
        self.assertEqual(212670, SubtlexCharData.objects.get(simplified='可').count)
        self.assertEqual(4848, SubtlexCharData.objects.get(simplified='环').count)

        # a check that our sample file hasn't changed
        data_set_size = SubtlexCharData.objects.all().aggregate(total=Sum('count'))['total']
        self.assertEqual(data_set_size, self.CHAR_SAMPLE_SET_SIZE)

        subtlex.update_char_freq_scores()

        self.assertEqual(self.NI_SAMPLE_COUNT, 
                         SubtlexCharData.objects.get(simplified='你').count)

        ni_percentage = float(self.NI_SAMPLE_COUNT) / float(self.CHAR_SAMPLE_SET_SIZE)
        
        self.assertLess(   ni_percentage, 0.04)
        self.assertGreater(ni_percentage, 0.03)
        self.assertEqual(760, subtlex.calc_frequency_score(4, 100))
        self.assertEqual(731, subtlex.calc_frequency_score(3, 100))
        self.assertLessEqual(Character.objects.get(char='你').freq_score, 760)
        self.assertGreaterEqual(Character.objects.get(char='你').freq_score, 731)


    def test_upload_word_data_and_compute_scores(self):
        subtlex.upload_subtlex_word_data(test_resource_file('subtlex_word_sample_set_1.csv'))
        self.assertEqual(1682530, SubtlexWordData.objects.get(simplified='的').count)
        self.assertEqual(236517, SubtlexWordData.objects.get(simplified='什么').count)
        self.assertEqual(59823, SubtlexWordData.objects.get(simplified='因为').count)
        self.assertEqual(2907, SubtlexWordData.objects.get(simplified='受到').count)

        # a check that our sample file hasn't changed
        data_set_size = SubtlexWordData.objects.all().aggregate(total=Sum('count'))['total']
        self.assertEqual(data_set_size, self.WORD_SAMPLE_SET_SIZE)

        subtlex.update_word_freq_scores()

        self.assertEqual(self.YINWEI_SAMPLE_COUNT, 
                         SubtlexWordData.objects.get(simplified='因为').count)

        yinwei_percentage = float(self.YINWEI_SAMPLE_COUNT) / float(self.WORD_SAMPLE_SET_SIZE)

        range_top = 22
        range_bot = 21
        denominator = 10000.0
        self.assertLess(   yinwei_percentage, float(range_top) / float(denominator))
        self.assertGreater(yinwei_percentage, float(range_bot) / float(denominator))
        self.assertEqual(470, subtlex.calc_frequency_score(range_top, denominator))
        self.assertEqual(466, subtlex.calc_frequency_score(range_bot, denominator))

        # check that a value in the expected range is in the Phrase freq_score
        self.assertLessEqual(ChinesePhrase.objects.get(simplified='因为').freq_score, 
                             subtlex.calc_frequency_score(range_top, denominator))
        self.assertGreaterEqual(ChinesePhrase.objects.get(simplified='因为').freq_score, 
                                subtlex.calc_frequency_score(range_bot, denominator))

        # check that a value in the expected range is in the Word freq_score
        self.assertLessEqual(ChineseWord.objects.get_simplified_exact('因为').freq_score, 
                             subtlex.calc_frequency_score(range_top, denominator))
        self.assertGreaterEqual(ChineseWord.objects.get_simplified_exact('因为').freq_score, 
                                subtlex.calc_frequency_score(range_bot, denominator))

        # check a single-char value in the expected range is in the Word freq_score
        self.assertEqual(self.ZAI_WORD_SAMPLE_COUNT, 
                         SubtlexWordData.objects.get(simplified='在').count)

        zai_percentage = float(self.ZAI_WORD_SAMPLE_COUNT) / float(self.WORD_SAMPLE_SET_SIZE)

        range_top = 160
        range_bot = 150
        denominator = 10000.0
        self.assertLess(   zai_percentage, float(range_top) / float(denominator))
        self.assertGreater(zai_percentage, float(range_bot) / float(denominator))
        self.assertEqual(668, subtlex.calc_frequency_score(range_top, denominator))
        self.assertEqual(662, subtlex.calc_frequency_score(range_bot, denominator))

        self.assertLessEqual(ChineseWord.objects.get_simplified_exact('在').freq_score, 
                             subtlex.calc_frequency_score(range_top, denominator))
        self.assertGreaterEqual(ChineseWord.objects.get_simplified_exact('在').freq_score, 
                                subtlex.calc_frequency_score(range_bot, denominator))

