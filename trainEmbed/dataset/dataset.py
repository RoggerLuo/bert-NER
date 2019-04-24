import numpy as np
from .db import Db


class Dataset(object):

    def __init__(self, config):
        self.config = config
        self.db = Db(config)
    
    def save(self):
        self.db.save()
        
    def get_negSamples(self):
        total_num = len(self.db.data)
        max_value = total_num - 1
        if max_value <= 0:return []

        # 如果可以选择的neg 还不够 要求的，那么，调整要求为最大可获得的neg_num
        neg_sample_num = self.config.neg_sample_num
        available_neg_num = total_num - 2
        if available_neg_num < self.config.neg_sample_num:
            neg_sample_num = available_neg_num

        negSamples = []
        while len(negSamples) < neg_sample_num - 1:
            randomEntry = self.db.data[np.random.randint(total_num)]
            if randomEntry['word'] != self.center['word']:
                if randomEntry['word'] != self.target['word']:
                    negSamples.append(randomEntry)
        return negSamples

    def get(self, center, target):  # TrainingPairs
        self.center = self.db.get_or_createEntryByWord(center)
        self.target = self.db.get_or_createEntryByWord(target)
        self.negSamples = self.get_negSamples()

        length = self.config.vector_dimsensions

        negs = [neg['vec'][length:] for neg in self.negSamples]  # 后一半vector
        # 前一半 后一半
        return self.center['vec'][:length], self.target['vec'][length:], negs

    def set(self, center, target, negSamples):
        length = self.config.vector_dimsensions
        self.center['vec'][:length] = center
        self.target['vec'][length:] = target
        for ind in range(len(negSamples)):
            self.negSamples[ind]['vec'][length:] = negSamples[ind]

