import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery
from python_translators.translators.wordnik_translator import WordnikTranslator
from python_translators.config import get_key_from_config


class TestWordnikTranslator(TestCase):

    def setUp(self):
        self.translator = WordnikTranslator(source_language='es',
                                            target_language='en',
                                            key=get_key_from_config('WORDNIK_API_KEY'))

    def testNumberOfTranslationsWorks(self):
        response = self.translator.translate(TranslationQuery(
            query="conjunction",
            max_translations=5
        ))

        assert 2 <= len(response.translations)

    def testUppercaseMatters(self):
        response = self.translator.translate(TranslationQuery(
            query="March",
            max_translations=5
        ))
        response2 = self.translator.translate(TranslationQuery(
            query="march",
            max_translations=5
        ))

        # The first is the month; the second is the verb
        assert response.translations != response2.translations

    def testWordnikShouldLowercaseByItself(self):
        response = self.translator.translate(TranslationQuery(
            query="Conjunction",
            max_translations=5
        ))

        self.assertFalse(response.translations == [])

    def testQuotedWord(self):
        response1 = self.translator.translate(TranslationQuery(
            query="'insincere'",
            max_translations=5
        ))

        response2 = self.translator.translate(TranslationQuery(
            query="insincere",
            max_translations=5
        ))

        response3 = self.translator.translate(TranslationQuery(
            query=''"insincere"'',
            max_translations=5
        ))

        assert (len(response1.translations) ==
                len(response2.translations) ==
                len(response3.translations))
