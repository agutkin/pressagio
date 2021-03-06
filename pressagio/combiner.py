"""
Combiner classes to merge results from several predictors.

"""
import abc

import pressagio.predictor


class Combiner(object):
    """
    Base class for all combiners
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def filter(self, prediction):
        seen_tokens = set()
        result = pressagio.predictor.Prediction()
        for i, suggestion in enumerate(prediction):
            token = suggestion.word
            if token not in seen_tokens:
                for j in range(i + 1, len(prediction)):
                    if token == prediction[j].word:
                        # TODO: interpolate here?
                        suggestion.probability += prediction[j].probability
                        if suggestion.probability > pressagio.predictor.MAX_PROBABILITY:
                            suggestion.probability = pressagio.MAX_PROBABILITY
                seen_tokens.add(token)
                result.add_suggestion(suggestion)
        return result

    @abc.abstractmethod
    def combine(self):
        raise NotImplementedError("Method must be implemented")


class MeritocracyCombiner(Combiner):
    def __init__(self):
        pass

    def combine(self, predictions):
        result = pressagio.predictor.Prediction()
        for prediction in predictions:
            for suggestion in prediction:
                result.add_suggestion(suggestion)
        return self.filter(result)
