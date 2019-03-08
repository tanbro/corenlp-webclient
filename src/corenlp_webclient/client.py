import codecs
import json
import os
from collections.abc import Iterable
from itertools import chain
from typing import Any, Optional, Union, List, Dict

import requests

from .annotators.baseannotator import BaseAnnotator
from .annotators.utils import make_properties
from .helpers import rm_cjk_space, bakcup_emoji, restore_emoji

__all__ = ['CoreNlpWebClient', 'chain_words', 'WORD_SEP', 'join_chain_words', 'extract_words', 'join_extract_words']


class CoreNlpWebClient:
    def __init__(self, url: str, session: Optional[requests.Session] = None):
        self._url = url
        self._session = session

    def api_call(self, text: str, annotators: Union[List[BaseAnnotator], BaseAnnotator, None] = None):
        text = text.strip()
        text = rm_cjk_space(text)
        text, emoji_map = bakcup_emoji(text)
        if annotators is None:
            annotators = list()
        elif not isinstance(annotators, Iterable):
            annotators = (annotators,)
        properties = make_properties(*annotators)
        if self._session:
            sender = self._session
        else:
            sender = requests
        response = sender.post(
            self._url,
            params={'properties': json.dumps(properties)},
            data=codecs.encode(text, 'utf-8'),
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        restore_emoji(data, emoji_map)
        return data


def chain_words(data: Dict[str, Any]) -> List[str]:
    return [
        token['word']
        for token in chain.from_iterable(
            sent['tokens'] for sent in data['sentences']
        )
    ]


WORD_SEP = ' '


def join_chain_words(data: Dict[str, Any], s: str = WORD_SEP) -> str:
    return s.join(chain_words(data))


def extract_words(data: Dict[str, Any]) -> List[List[str]]:
    result = list()
    for sent in data['sentences']:
        ls = list()
        for token_obj in sent['tokens']:
            ls.append(token_obj['word'])
        result.append(ls)
    return result


def join_extract_words(data: Dict[str, Any], word_sep: str = WORD_SEP, line_sep=os.linesep) -> str:
    result = list()
    for sent in data['sentences']:
        ls = list()
        for token_obj in sent['tokens']:
            ls.append(token_obj['word'])
        result.append(word_sep.join(ls))
    return line_sep.join(result)
