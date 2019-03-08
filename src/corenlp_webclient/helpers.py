import os
import re
from itertools import chain
from typing import Any, Dict, List, Tuple

from emoji_data import EmojiData

EmojiData.initial()

REPLACEMENT = chr(0xFFFD)

REGEX_CJK_SPACE = re.compile(r'(?P<c>[\u2E80-\u9FFF])(\s+)')


def rm_cjk_space(s):  # type: (str)->str
    """消除中文之间的空格

    中文之间的空格会影响 CoreNLP 分词!
    """
    return REGEX_CJK_SPACE.sub(r'\g<c>', s.strip())


def rm_emoji(s):  # type: (str)->str
    return EmojiData.get_regex_pattern().sub('', s)


def backup_emoji(text: str) -> Tuple[str, Dict[int, str]]:
    """Replace emoji chars(Some emoji won't be properly processed by core nlp！) by U+FFFD,
    then returns the replaced text and a Position->Char backup map for restoring later.

    :param text: replace emoji in the text
    :return: replaced text and original emoji's position-chat backup map
    """
    stack = dict()
    new_text = ''
    for i, c in enumerate(text):
        if ord(c) in EmojiData:
            stack[i] = c
            new_text += REPLACEMENT
        else:
            new_text += c
    return new_text, stack


def restore_emoji(data: Dict[str, Any], emoji_map: Dict[int, str]):
    if not emoji_map:
        return
    for sentence_obj in data['sentences']:
        for token_obj in sentence_obj['tokens']:
            word = ''
            for i, c, in enumerate(token_obj['word']):
                emoji = emoji_map.get(
                    i + token_obj['characterOffsetBegin'], None)
                if emoji:
                    word += emoji
                else:
                    word += c
            token_obj['word'] = word


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
        toks = list()
        for token_obj in sent['tokens']:
            toks.append(token_obj['word'])
        result.append(toks)
    return result


def join_extract_words(data: Dict[str, Any], word_sep: str = WORD_SEP, line_sep=os.linesep) -> str:
    result = list()
    for sent in data['sentences']:
        toks = list()
        for token_obj in sent['tokens']:
            toks.append(token_obj['word'])
        result.append(word_sep.join(toks))
    return line_sep.join(result)
