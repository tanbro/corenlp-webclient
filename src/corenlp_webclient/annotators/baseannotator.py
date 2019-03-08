from typing import Any, Dict, Optional

from ..options.baseoptions import BaseOptions


class BaseAnnotator: # pylint:disable=too-few-public-methods
    name = ''

    def __init__(self, options: Optional[BaseOptions] = None):
        self.options = options

    def make_options_dict(self)->Dict[str, Any]:
        if not self.options:
            return dict()
        return {'.'.join([self.name, k]): v for k, v in self.options.to_dict().items()}
