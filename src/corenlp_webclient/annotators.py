from typing import Any, Dict, Optional, Type

from .options import BaseOptions, WordsToSentenceOptions

__all__ = ['BaseAnnotator', 'WordsToSentenceAnnotator']


def _snake_to_camel(s):  # type: (str)->str
    parts = s.strip().split('_')
    return parts[0] + ''.join([w.title() for w in parts])


class BaseAnnotator:  # pylint:disable=too-few-public-methods
    name: str = ''
    options_class: Type[BaseOptions] = BaseOptions

    def __init__(self, options: Optional[BaseOptions] = None):
        self._options = options
        self._options_dict = {}

    def get_options_dict(self) -> Dict[str, Any]:
        if self._options_dict:
            return self._options_dict
        if self._options:
            self._options_dict = {
                '.'.join([self.name, _snake_to_camel(k)]): v
                for k, v in self._options.to_dict().items()
            }
        return self._options_dict

    @property
    def options_dict(self) -> Dict[str, Any]:
        return self.get_options_dict()


class WordsToSentenceAnnotator(BaseAnnotator):  # pylint:disable=too-few-public-methods
    name = 'ssplit'
    options_class = WordsToSentenceOptions
