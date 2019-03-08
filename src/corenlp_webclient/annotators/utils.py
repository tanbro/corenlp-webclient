from typing import Any, Dict

from .baseannotator import BaseAnnotator


def make_properties(*annotators: BaseAnnotator)->Dict[str, Any]:
    properties_dict = {'outputFormat': 'json'}
    for annotator in annotators:
        if 'annotators' not in properties_dict:
            properties_dict['annotators'] = annotator.name
        else:
            properties_dict['annotators'] += ',{}'.format(annotator.name)
        options_dict = annotator.make_options_dict()
        if options_dict:
            properties_dict.update(options_dict)
    return properties_dict