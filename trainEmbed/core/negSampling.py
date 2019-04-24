import numpy as np


class NegSampling(object):

    def __init__(self, config):
        self.config = config

    # center 固定不变的信号输入,
    # target 被修改的 node embeding
    # “n”是指 negative words

    # 拉近 外界输入信息embed和node embed
    # 每个node中的神经网络 才是这个 “node embed"吧，
    
    # 现在做的功能，拉近两个embed，就是作为分类功能的node（node就是一个小型神经网络），
    # 训练这个神经网络，让这个node变成某种概念的筛选器，训练完成后，
    # 使用这个筛选器，就能够判断 任意一个外界的输入信息（词汇） 是否符合、属于、靠近这个概念

    # 所有的神经网络size可以和embed不同， 大于还是小于呢 
    # w2v其实也可以看成 每个词都有一个神经网络，w2v的训练过程正是训练它们的中间层，w2v的使用正是使用它训练好的模型

    def train(self, inputWordEmbeding, nodeEmbeding, n):
        step = self.config.learning_rate
        ___cost, ___c_grad, grad_of_nodeEmbeding, ___n_grad = self.getGrad(inputWordEmbeding, nodeEmbeding, n)
        
        # inputWordEmbeding = inputWordEmbeding - ___c_grad * step # 不用更新inputWordEmbeding
        

        # 更新nodeEmbeding
        nodeEmbeding = nodeEmbeding - grad_of_nodeEmbeding * step
        
        for index in range(len(n)):
            neg = n[index]
            neg_grad = ___n_grad[index]
            neg = neg - neg_grad * step
            n[index] = neg  # 保险？
        return c, t, n, ___cost

    def getGrad(self, c, t, n):
        dotProduct = np.sum(t * c)
        ct_activ = self.sigmoid(dotProduct)
        
        ___cost = - np.log(ct_activ)        
        ___c_grad = self.calcGrad(ct_activ, t)
        ___t_grad = self.calcGrad(ct_activ, c)
        ___n_grad = []

        for neg in n:
            dotProduct = np.sum(neg * c)
            cn_activ = self.sigmoid(-dotProduct)

            ___cost -= np.log(cn_activ)  # cost 第二弹

            # centerword grad 第二弹
            ___c_grad -= self.calcGrad(cn_activ, neg)

            neg_grad = - self.calcGrad(cn_activ, c)
            ___n_grad.append(neg_grad)

        return ___cost, ___c_grad, ___t_grad, ___n_grad

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def calcGrad(self, activation, vector):
        deviation = activation - 1
        grad = deviation * vector
        return grad
