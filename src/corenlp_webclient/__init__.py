from .annotators.ssplit import WordsToSentenceAnnotator
from .client import CoreNlpWebClient, chain_words, join_chain_words, extract_words, join_extract_words
from .options.ssplit import NewlineIsSentenceBreak, WordsToSentenceOptions
from .version import version as __version__
