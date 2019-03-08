from typing import Any, Dict, Optional

from ..options.baseoptions import BaseOptions


class BaseAnnotator:  # pylint:disable=too-few-public-methods
    name = ''
    options_class = BaseOptions

    def __init__(self, options: Optional[BaseOptions] = None):
        self._options = options

    def make_options_dict(self) -> Dict[str, Any]:
        if not self._options:
            return dict()
        return {'.'.join([self.name, k]): v for k, v in self._options.to_dict().items()}
