import re
from typing import Any, Dict, Tuple

from emoji_data import EmojiData

EmojiData.initial()

REPLACEMENT = chr(0xFFFD)

REGEX_CJK_SPACE = re.compile(r'(?P<c>[\u2E80-\u9FFF])(\s+)')


def rm_cjk_space(s):  # type: (str)->str
    """消除中文之间的空格

    中文之间的空格会影响 CoreNLP 分词!
    """
    return REGEX_CJK_SPACE.sub(r'\g<c>', s.strip())


def bakcup_emoji(text: str) -> Tuple[str, Dict[int, str]]:
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
            emojis = ''
            for i in range(token_obj['characterOffsetBegin'], token_obj['characterOffsetEnd']):
                emoji = emoji_map.get(i, None)
                if emoji:
                    emojis += emoji
            if emojis:
                token_obj['word'] = token_obj['originalText'] = emojis
