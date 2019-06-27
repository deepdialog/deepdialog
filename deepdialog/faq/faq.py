# -*- coding: utf-8 -*-
"""FAQ Module."""

import os
import yaml
from yaml import Loader
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
from ..common.component import Component


def tokenizer(x):
    """Tokenize sentence."""
    return list(x)


class FrequentlyAskedQuestions(Component):
    """FAQ Module."""

    def __init__(self):
        """Init FAQ."""
        self.data = None
        self.tfidf = None
        self.vecs = None
        self.questions = None

    def __len__(self):
        """Return length of data."""
        return len(self.data) if self.data else 0

    def fit(self, data_path):
        """Fit the FAQ."""
        if not os.path.exists(data_path):
            return
        exists = {}
        data = []
        # for dirname, _, names in os.walk(data_path):
        #     names = [x for x in names if x.lower().endswith('.yml')]
        #     for name in names:
        #         path = os.path.join(dirname, name)
        #         obj = yaml.load(open(path), Loader=Loader)
        #         assert isinstance(obj, dict)
        #         for k, v in obj.items():
        #             assert k not in exists
        #             exists[k] = True
        #             data.append((k, v))
        obj = yaml.load(open(data_path), Loader=Loader)
        assert isinstance(obj, dict)
        assert 'faq' in obj
        for item in obj.get('faq'):
            assert 'question' in item
            assert 'answer' in item
            k = item.get('question')
            v = item.get('answer')
            assert k not in exists
            exists[k] = True
            data.append((k, v))
        self.data = data
        self.questions = [x[0] for x in data]
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            tokenizer=tokenizer)
        self.tfidf.fit(self.questions)
        self.vecs = self.tfidf.transform(self.questions).toarray()

    def forward(self, question):
        """Predict."""
        vec = self.tfidf.transform([question]).toarray().flatten()
        answer = None
        max_distance = None
        for v, p in zip(self.vecs, self.data):
            distance = cosine(vec, v)
            if max_distance is None or distance < max_distance:
                max_distance = distance
                answer = p[1]
        return answer
