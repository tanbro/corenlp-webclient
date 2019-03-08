from typing import Optional

from .baseannotator import BaseAnnotator
from ..options.ssplit import WordsToSentenceOptions

__all__ = ['WordsToSentenceAnnotator']


class WordsToSentenceAnnotator(BaseAnnotator):  # pylint:disable=too-few-public-methods
    name = 'ssplit'

    def __init__(self, options: Optional[WordsToSentenceOptions] = None):
        if options is None:
            options = WordsToSentenceOptions()
        super().__init__(options=options)
