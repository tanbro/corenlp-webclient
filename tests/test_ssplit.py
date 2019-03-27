import os
import unittest

from corenlp_webclient import (CoreNlpWebClient, WordsToSentenceAnnotator,
                               create_annotator, join_chain_words,
                               join_extract_words)

URL = os.environ['CORENLP_SERVER_URL']


def make_annotator(*args, **kwargs):
    return create_annotator(WordsToSentenceAnnotator, *args, **kwargs)


class SsplitTestCase(unittest.TestCase):

    def test_one_simple_no_annotator(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗
        '''
        result = CoreNlpWebClient(URL).api_call(text)
        self.assertEqual(join_chain_words(result), segmented.strip())

    def test_one_simple_no_options(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗
        '''
        result = CoreNlpWebClient(URL).api_call(text, make_annotator())
        self.assertEqual(join_chain_words(result), segmented.strip())

    def test_one_simple_twice(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗
        '''
        client = CoreNlpWebClient(URL)
        annotator = make_annotator()
        for _ in range(2):
            result = client.api_call(text, annotator)
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
            make_annotator(boundary_token_regex=r'[.。]|[!?！？]+')
        )
        self.assertEqual(len(result['sentences']), 2)
        self.assertEqual(join_extract_words(result), segmented.strip())

    def test_two_with_zh_boundary_twice(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗。狗却没有反应。
        '''
        segmented = '''
快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 。
狗 却 没有 反应 。
        '''
        client = CoreNlpWebClient(URL)
        annotator = make_annotator(boundary_token_regex=r'[.。]|[!?！？]+')
        for _ in range(2):
            result = client.api_call(text, annotator)
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
            make_annotator()
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
            text, make_annotator(boundary_token_regex=r'[.。]|[!?！？]+'))
        self.assertEqual(join_chain_words(result), segmented.strip())
        self.assertEqual(len(result['sentences']), 1)

    def test_one_has_comma_without_zh_boundary(self):
        text = '''
        快速的棕色狐狸跳过了懒惰的狗，狗却没有反应。
        '''
        segmented = '''
        快速 的 棕色 狐狸 跳过 了 懒惰 的 狗 ， 狗 却 没有 反应 。
        '''
        result = CoreNlpWebClient(URL).api_call(text, make_annotator())
        self.assertEqual(join_chain_words(result), segmented.strip())
        self.assertEqual(len(result['sentences']), 1)


if __name__ == '__main__':
    unittest.main()
