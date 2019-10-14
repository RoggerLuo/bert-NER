import os
from data_loader import DataLoader
import argparse
import utils
import torch
import random
import logging

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default='data/msra/', help="Directory containing the dataset")
parser.add_argument('--bert_model_dir', default='bert-base-chinese-pytorch', help="Directory containing the BERT model in PyTorch")
parser.add_argument('--model_dir', default='experiments/base_model', help="Directory containing params.json")
parser.add_argument('--seed', type=int, default=23, help="random seed for initialization")
parser.add_argument('--restore_file', default='best', help="name of the file in `model_dir` containing weights to load")
parser.add_argument('--multi_gpu', default=False, action='store_true', help="Whether to use multiple GPUs if available")
parser.add_argument('--fp16', default=False, action='store_true', help="Whether to use 16-bit float precision instead of 32-bit")
args = parser.parse_args()

params= {

}
def load_tags():
    tags = []
    file_path = os.path.join(args.data_dir, 'tags.txt')
    with open(file_path, 'r') as file:
        for tag in file:
            tags.append(tag.strip())
    return tags

# data_loader = DataLoader(args['data_dir'], args['bert_model_dir'], params, token_pad_idx=0)
tags = load_tags()
""" key同样也可以是变量 """
""" for循环的简写，可以用在dict里面 """
tag2idx = {tag: idx for idx, tag in enumerate(tags)}
idx2tag = {idx: tag for idx, tag in enumerate(tags)}


# print(tags)
# print(tag2idx)
# print(idx2tag)


json_path = os.path.join(args.model_dir, 'params.json')
params = utils.Params(json_path)
params.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
params.n_gpu = torch.cuda.device_count()
params.multi_gpu = args.multi_gpu
random.seed(args.seed)
torch.manual_seed(args.seed)
if params.n_gpu > 0:
    torch.cuda.manual_seed_all(args.seed)  # set random seed for all GPUs
params.seed = args.seed
utils.set_logger(os.path.join(args.model_dir, 'testrun.log'))
logging.info("Loading the dataset...")
data_loader = DataLoader(args.data_dir, args.bert_model_dir, params, token_pad_idx=0)
test_data = data_loader.load_data('test')
""" 
{
    data:[[ idx ]],
    tags:[[ idx ]],
    size: len(data)
}

"""
params.test_size = test_data['size']
params.eval_steps = params.test_size // params.batch_size
test_data_iterator = data_loader.data_iterator(test_data, shuffle=False)


for _ in range(params.eval_steps):
    batch_data, batch_tags = next(test_data_iterator)
    print(_)
    """ 
    torch.Size([ batch_size , 40(sentence length) ])
    """

""" 
BertForTokenClassification:
如果labels不是None（训练时）：输出的是分类的交叉熵
如果labels是None（评价时）：输出的是shape为[batch_size, num_labels]估计值
"""

# Define the model
config_path = os.path.join(args.bert_model_dir, 'bert_config.json')
config = BertConfig.from_json_file(config_path)
model = BertForTokenClassification(config, num_labels=len(params.tag2idx))

model.to(params.device)
