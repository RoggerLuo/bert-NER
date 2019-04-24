import numpy as np

center = np.array([1, 2, 3])
target = np.array([4, 5, 6])
negs = [np.array([7, 8, 9]), np.array([3, 6, 9])]

class Wv(object):

    def __init__(self, config):
        self.config = config

    def getStartVector(self):
        randomVec = (np.random.rand(self.config.vector_dimsensions) - 0.5)
        zerosVector = np.zeros((self.config.vector_dimsensions))
        return np.concatenate((randomVec / self.config.vector_dimsensions, zerosVector), axis=0)

def test():
    class Config(object):
        vector_dimsensions = 2
    wv = Wv(Config)
    print(wv.getStartVector())

# test()
