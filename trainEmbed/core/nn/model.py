import tensorflow as tf
import numpy as np
from .op_cost import get_cost
import time


class Nn(object):

    def __init__(self, config):
        self.config = config

    def build(self, center, target, negs):
        self.center = tf.Variable(center, dtype=tf.float32)
        self.target = tf.Variable(target, dtype=tf.float32)
        self.negs = list(
            map(lambda neg: tf.Variable(neg, dtype=tf.float32), negs))
        self.sess = tf.Session()
        self.rs_list = []

        self.cost = get_cost(self.center, self.target, self.negs)
        self.gd = tf.train.GradientDescentOptimizer(
            self.config.learning_rate).minimize(self.cost)
        return self

    def train(self):
        init_op = tf.global_variables_initializer()
        self.sess.run(init_op)
        for i in range(self.config.repeate_times):
            self.sess.run(self.gd)

            # 调参数、测试性能的时候才调用
            # self.rs_list.append(self.sess.run(self.cost))
        return self

    def export(self):
        center = self.sess.run(self.center)
        target = self.sess.run(self.target)
        negs = [self.sess.run(neg) for neg in self.negs]
        return center, target, negs, self.rs_list


def test():
    class Config(object):
        repeate_times = 10

    center = np.array([1, 2, 3])
    target = np.array([4, 5, 6])
    negs = [np.array([7, 8, 9]), np.array([3, 6, 9])]

    # running test
    nn = Nn(Config)
    center, target, negs, rs_list = nn.build(
        center, target, negs).train().export()
    print(rs_list)
    print(center)
    print(target)
    print(negs)
    show(rs_list)

# test()
