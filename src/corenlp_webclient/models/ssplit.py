from typing import Optional, List, Dict, NewType, Any, Tuple, Union
from dataclasses import asdict, fields, dataclass
from enum import Enum

from dataclasses_jsonschema import JsonSchemaMixin


class NewlineIsSentenceBreak(Enum):
    """Whether to treat newlines as sentence breaks    
    """
    ALWAYS = 'always'
    NEVER = 'never'
    TWO = 'two'


@dataclass
class Options(JsonSchemaMixin):
    """Options of Words-To-Sentence Annotator

    see: https://stanfordnlp.github.io/CoreNLP/ssplit.html
    """
    eolonly: bool = False
    isOneSentence: bool = False
    newlineIsSentenceBreak: NewlineIsSentenceBreak = NewlineIsSentenceBreak.NEVER
    boundaryMultiTokenRegex: str = None
    boundariesToDiscard: List[str] = None
    htmlBoundariesToDiscard: str = None
    tokenPatternsToDiscard: List(str) = None
    boundaryFollowersRegex: str = None
