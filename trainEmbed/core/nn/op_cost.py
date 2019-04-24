import tensorflow as tf
import numpy as np


def grad_closer(a, b):
    # a、b为 n-dimensional vector
    x = tf.transpose(tf.expand_dims(b, 1))
    y = tf.expand_dims(a, 1)
    dot = tf.matmul(x, y)
    # 相乘越大 越接近1， log的绝对值越小(0,1)， -log的值越小， cost越小
    activated_dot = tf.sigmoid(dot)
    return (- tf.log(activated_dot))


def grad_farther(a, b):
    # a、b为 n-dimensional vector
    x = tf.transpose(tf.expand_dims(b, 1))
    y = tf.expand_dims(a, 1)
    dot = tf.matmul(x, y)
    activated_dot = tf.sigmoid(- dot)
    return (- tf.log(activated_dot))


def get_cost(centerword, targetword, negwords):
    # centerword 为 n-dimensional vector (tf.variable)
    # targetword 为 n-dimensional vector (tf.variable)
    # negwords 为 n-dimensional vector的list (tf.variable)

    # 循环所有negwords
    negword_costs = [grad_farther(centerword, negword) for negword in negwords]
    # 把cost加起来
    J_negSample = grad_closer(centerword, targetword) + tf.reduce_sum(negword_costs)
    J_negSample = tf.reduce_sum(J_negSample)
    return J_negSample


def test():
    centerword = tf.Variable(np.array([1, 2, 3]), dtype=tf.float32)
    targetword = tf.Variable(np.array([4, 5, 6]), dtype=tf.float32)
    negwords = [
        tf.Variable(np.array([7, 8, 9]), dtype=tf.float32),
        tf.Variable(np.array([3, 6, 9]), dtype=tf.float32)
    ]
    sess = tf.Session()
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    #  get cost 测试
    print(sess.run(grad_closer(centerword, targetword)))
    print(sess.run(grad_farther(centerword, targetword)))
    print(sess.run(get_cost(centerword, targetword, negwords)))

