from ..options.ssplit import WordsToSentenceOptions
from .baseannotator import BaseAnnotator

__all__ = ['WordsToSentenceAnnotator']


class WordsToSentenceAnnotator(BaseAnnotator):  # pylint:disable=too-few-public-methods
    name = 'ssplit'
    options_class = WordsToSentenceOptions
