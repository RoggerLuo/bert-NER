import os
import numpy as np
import pickle
from .wv import Wv  # 也许可以不用初始化多个Wv实例，到时候再处理

# 数据格式 {'vec','word'}


class Db(object):

    def __init__(self, config):
        self.config = config
        self.wv = Wv(config)
        
        if os.path.exists(self.config.db_path):
            with open(self.config.db_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = []

    def save(self):
        with open(self.config.db_path, 'wb') as f:
            pickle.dump(self.data, f, True)

    def getEntrysByWord(self,word):
        return list(filter(lambda e: e['word'] == word, self.data))

    def get_or_createEntryByWord(self, word):
        rs = list(filter(lambda e: e['word'] == word, self.data))
        if len(rs) == 0:  # 没找到
            newEntry = {'vec': self.wv.getStartVector(), 'word': word}
            self.data.append(newEntry)
            return newEntry
        return rs[0]


def test1():     # 读取 、 创建entry
    class Config(object):
        db_path = './db.pkl'
        vector_dimsensions = 8

    db = Db(Config)
    print(db.getEntryByWord('roger'))
    db.write_pkl()
    db2 = Db(Config)
    print(db2.getEntryByWord('roger'))


def test2():  # 测试引用传递
    class Config(object):
        db_path = './db.pkl'
        vector_dimsensions = 8

    db = Db(Config)
    roger = db.getEntryByWord('roger')
    print(db.data)
    roger['vec'][0] = 0.1
    print(db.data)
