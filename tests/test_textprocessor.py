import unittest
from src.exercise import SentProcessor, Exercise
import numpy
from pymorphy2.tagset import OpencorporaTag
from src.word import Word


class SentProcessorBaseTests(unittest.TestCase):

    def test_getrawtext(self):
        sentences = ['Кошка спит на диване', 'Кошка спит', 'кошка,,,,, спит.....']
        for sent in sentences:
            instance = SentProcessor(sent)
            self.assertEqual(instance.get_raw_text(), sent)

    def test_getrawtext_corrupted(self):
        instance = SentProcessor(None)
        self.assertEqual(instance.get_raw_text(), None)

    def test_getrawinput_incorrect_input(self):
        sentences = [123, ('Кошка спит', ), [None]]
        for sent in sentences:
            instance = SentProcessor(sent)
            self.assertEqual(instance.get_raw_text(), None)

    def test_tokenise(self):
        instance = SentProcessor('Кошка спит на диване!')
        instance.process_text()
        self.assertEqual(instance._tokens, ['кошка', 'спит', 'на', 'диване'])

    def test_vectorise(self):
        sentences = ['Кошка', 'stjrdvrdjfvkjy']
        for sent in sentences:
            instance = SentProcessor(sent)
            instance.process_text()
            self.assertEqual(type(instance._vector[sent.lower()]), numpy.ndarray)

    def test_vectorise_corrupted_input(self):
        instance = SentProcessor('')
        instance.process_text()
        self.assertEqual(instance._vector, {})

    def test_get_vectors_access_check(self):
        instance = SentProcessor('кошка')
        instance._vector = 0
        self.assertEqual(instance.get_vectors(), 0)

    def test_get_vectors_type_check(self):
        instance = SentProcessor('кошка')
        instance.process_text()
        self.assertEqual(type(instance.get_vectors()['кошка']), numpy.ndarray)
        self.assertEqual(type(instance.get_vectors()), dict)

    def test_process_text_values(self):
        instance = SentProcessor('Кошка спит на диване 0!')
        instance.process_text()
        self.assertEqual(instance._tokens, ['кошка', 'спит', 'на', 'диване', '0'])
        self.assertEqual(instance._lemma_text, ['кошка', 'спать', 'на', 'диван', '0'])
        self.assertEqual(instance._morph, [OpencorporaTag('NOUN,anim,femn sing,nomn'),
                                                OpencorporaTag('VERB,impf,intr sing,3per,pres,indc'),
                                                OpencorporaTag('PREP'),
                                                OpencorporaTag('NOUN,inan,masc sing,loct'),
                                                OpencorporaTag('NUMB,intg')])
        for vector in instance._vector.values():
            self.assertEqual(type(vector), numpy.ndarray)

    def test_process_text_types(self):
        instance = SentProcessor('Кошка спит на диване 0!')
        instance.process_text()
        self.assertEqual(type(instance.get_tokens()[0]), str)
        self.assertEqual(type(instance.get_lemmas()[0]), str)
        self.assertEqual(type(instance.get_morph()[0]), OpencorporaTag)
        self.assertEqual(type(instance.get_vectors()['кошка']), numpy.ndarray)

        self.assertEqual(type(instance.get_tokens()), list)
        self.assertEqual(type(instance.get_lemmas()), list)
        self.assertEqual(type(instance.get_morph()), list)
        self.assertEqual(type(instance.get_vectors()), dict)


class ExerciseBaseTests(unittest.TestCase):

    def test_select_grammatical_form(self):
        sents = []
        sent = SentProcessor('Кошка спит.')
        sent.process_text()
        sents.append(sent)
        ex = Exercise(sents)
        ex.select_grammatical_form(1)
        self.assertEqual(ex.fifth_ex , '_____ [кошка] _____ [спать].\n')
        self.assertEqual(ex.fifth_answers, 'Кошка спит.\n')

    def test_find_collocations(self):
        sents = []
        sent = SentProcessor('Кошка спит.')
        sent.process_text()
        sents.append(sent)
        ex = Exercise(sents)
        ex.find_collocations(1)
        self.assertEqual(ex.sixth_ex, '_____[девочка, животное, кошка, птица, рыба, собака] спит.\n')
        self.assertEqual(ex.sixth_answers, '\nКошка спит.')

    def test_antonyms(self):
        word = Word('холодный', 0)
        word.extract_synonyms_antonyms('холодный')
        test_value = False
        correct = {'нехолодный', 'теплый по цвету', 'теплый'}
        if all(correct) in word.get_antonyms():
            test_value = True
        msg = 'Something is wrong'
        self.assertTrue(test_value, msg)

    def test_synonyms(self):
        word = Word('холодный', 0)
        word.extract_synonyms_antonyms('холодный')
        correct = {'ледяной', 'студёный', 'холодный'}
        test_value = False
        if all(correct) in word.get_synonyms():
            test_value = True
        msg = 'Something is wrong'
        self.assertTrue(test_value, msg)
