import os
import unittest

from dotenv import load_dotenv

from corenlp_webclient import CoreNlpWebClient, WordsToSentenceAnnotator, WordsToSentenceOptions, \
    join_chain_words, join_extract_words

load_dotenv()
URL = os.environ['CORENLP_SERVER_URL']


class SsplitTestCase(unittest.TestCase):
    def test_one_simple_no_options(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗
        '''
        result = CoreNlpWebClient(URL).api_call(text, WordsToSentenceAnnotator())
        self.assertEqual(join_chain_words(result), segmented.strip())

    def test_two_with_zh_boundary(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗。狗却没有反应。
        '''
        segmented = '''
快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 。
狗 却 没有 反应 。
        '''
        result = CoreNlpWebClient(URL).api_call(
            text,
            WordsToSentenceAnnotator(WordsToSentenceOptions(boundaryTokenRegex=r'[.。]|[!?！？]+'))
        )
        self.assertEqual(len(result['sentences']), 2)
        self.assertEqual(join_extract_words(result), segmented.strip())

    def test_two_without_zh_boundary(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗。狗却没有反应。
        '''
        segmented = '''
快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 。
狗 却 没有 反应 。
        '''
        result = CoreNlpWebClient(URL).api_call(
            text,
            WordsToSentenceAnnotator(WordsToSentenceOptions())
        )
        self.assertEqual(len(result['sentences']), 2)
        self.assertEqual(join_extract_words(result), segmented.strip())

    def test_one_has_comma_with_zh_boundary(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗，狗却没有反应。
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 ， 狗 却 没有 反应 。
        '''
        result = CoreNlpWebClient(URL).api_call(
            text,
            WordsToSentenceAnnotator(WordsToSentenceOptions(boundaryTokenRegex=r'[.。]|[!?！？]+'))
        )
        self.assertEqual(join_chain_words(result), segmented.strip())
        self.assertEqual(len(result['sentences']), 1)

    def test_one_has_comma_without_zh_boundary(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗，狗却没有反应。
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 ， 狗 却 没有 反应 。
        '''
        result = CoreNlpWebClient(URL).api_call(
            text,
            WordsToSentenceAnnotator(WordsToSentenceOptions())
        )
        self.assertEqual(join_chain_words(result), segmented.strip())
        self.assertEqual(len(result['sentences']), 1)

    def test_one_simple_with_emoji(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的🐕
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 🐕
        '''
        result = CoreNlpWebClient(URL).api_call(text, WordsToSentenceAnnotator())
        self.assertEqual(join_chain_words(result), segmented.strip())


if __name__ == '__main__':
    unittest.main()
