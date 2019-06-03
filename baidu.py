# pip install baidu-aip
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '15737243'
API_KEY = 'MmGcFmcpYeG6vEKEBc20K9zP'
SECRET_KEY = 'fGLes8qGvGrntH1Cx75hnSXoGK5dgmcN'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


word = "张飞"

""" 调用词向量表示 """
emb = client.wordEmbedding(word)
print(len(emb['vec']))
