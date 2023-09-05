import pandas as pd
import numpy as np
from model import *
from model import *
from analysis import *

import re

def ds_processing(input_df, question_dict_dict):
    neural_net = current_model()
    new_df = input_df.apply(lambda row: iterate_one_dict(row, question_dict_dict, neural_net), axis=1)
    return new_df