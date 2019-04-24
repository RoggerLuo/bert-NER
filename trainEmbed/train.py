# from .config import Config
from .dataset.dataset import Dataset
from .core.nn.model import Nn
from .core.negSampling import NegSampling
import numpy as np
import time
timeRecorder = 0


class Train(object):

    def __init__(self, config):
        self.dataset = Dataset(config)
        self.nn = Nn(config)
        self.negSampling = NegSampling(config)
        self.config = config

    def wordlist(self, wordlist):
        word_n_context_pairs = self.getWordAndContext(wordlist)
        cost = 0
        for pair in word_n_context_pairs:
            cost += self.centerword_n_context_pair(pair)
        return cost

    def getWordAndContext(self, wordlist):
        word_n_context_pairs = []
        c = self.config.window_size
        counts = len(wordlist)
        for index in range(counts):

            # 滑窗的start\end\index
            word = wordlist[index]
            start = index - c if (index - c) >= 0 else 0
            end = index + 1 + c if (index + 1 + c) <= counts else counts

            context = wordlist[start:index]  # 选中的词之前的
            context2 = wordlist[index + 1:end]  # 选中的词之后的
            context.extend(context2)

            # 用一个tuple表示
            item = {'word': word, 'context': context}
            word_n_context_pairs.append(item)
        return word_n_context_pairs

    def centerword_n_context_pair(self, pair):
        center = pair['word']
        contexts = pair['context']
        # print('training word:', center)
        cost = 0
        for target in contexts:
            cost += self.center_n_target(center, target)
        return cost





    # center和target是两个词的string, start here
    # “n”是指 negative words
    def center_n_target(self, center, target):
        c, t, n = self.dataset.get(center, target)  # 换取得到word vector的值
        # c, t, n = self.tensorflow_nn(c, t, n)
        c, t, n, cost = self.native_nn(c, t, n)

        self.dataset.set(c, t, n)  # 保存回去
        return cost

    def native_nn(self, c, t, n):
        # timeRecorder = time.time()
        c, t, n, cost_list = self.negSampling.train(c, t, n)
        # print('train 耗时：', time.time() - timeRecorder)
        return c, t, n, cost_list

    def tensorflow_nn(self, c, t, n):
        timeRecorder = time.time()
        self.nn.build(c, t, n)  # 一组center target negs
        print('build 耗时：', time.time() - timeRecorder)

        timeRecorder = time.time()
        c, t, n, cost_list = self.nn.train().export()
        print('train 耗时：', time.time() - timeRecorder)
        return c, t, n

    def save(self):
        self.dataset.save()

