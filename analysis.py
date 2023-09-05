import pandas as pd
import numpy as np
from model import *
from util import *
import string
import time

import re



#input_df = pd.read_csv('C:/Users/daria/Documents/llm_cardio/medtextscan_test_5')

'''question_dict_dict = {'ObObsl':{'numeric':['Какой рост?','Какой вес?','Какой индекс массы тела (ИМТ)?',''],'binary':[]},
'Oper':{'numeric':['Какова степень ФК стенокардии?'],'binary':['Есть сахарный диабет?','Есть инсулинзависимый сахарный диабет?', 'Есть ли артериальная гипертензия?']}}
'''
#question_dict_dict = {'ObObsl':{'numeric':['Какой рост?'],'binary':[]}}



def parse_binary_answer(answer,log_cls):
    str0 = answer.translate(str.maketrans('', '', string.punctuation))
    if 'Да' in str0.split():
        log_cls.write_log(message='OK', model_answer=answer)
        return 1
    if 'Нет' in str0.split():
        log_cls.write_log(message='OK', model_answer=answer)
        return 0
    else:
        log_cls.write_log(message = 'Слова Да Нет не найдены в ответе модели', model_answer = answer)
        return np.NaN


def find_numerical(answer, log_cls):
    float_list = []
    float_list = re.findall(r"[-+]?(?:\d*\.*\d+)", answer)
    if len(float_list) == 0:
        log_cls.write_log(message='Числовое значение (целое или дробное) не найдено в ответе модели', model_answer=answer)
        return np.NaN
    else:
        log_cls.write_log(message='OK', model_answer=answer)
        return float(float_list[0])


def clean_answer(nn_string):
    result_str = nn_string.replace("<pad><extra_id_0>", "")
    result_str = result_str.replace("</s>", "")
    return result_str


def iterate_one_dict(row, question_dict, neural_net):
    print(row.name)
    log_cls = log()
    d = {'numeric': find_numerical, 'binary': parse_binary_answer}
    df_list = []
    df_names = []
    for k, v in question_dict.items():
        n=0
        for box_cat, question_list in v.items():
            for question in question_list:
                n = n + 1
                new_col_name = str(k) + '_' + 'вопрос' + str(n) + '_' + box_cat
                if pd.isna(row[k]):
                    log_cls.write_log(message='Входные данные NaN', model_answer='Модель не запускалась')
                    ans = 'NaN'
                else:
                    prompt = '''<SC6>Текст: {}\nВопрос: {}\nОтвет: <extra_id_0>
                    '''.format(str(row[k]), str(question))
                    neural_net_res = neural_net.generate(prompt, log_cls)
                    ans0 = neural_net_res
                    ans_ = clean_answer(ans0)
                    ans = d[box_cat](ans_, log_cls)
                df_list.append(ans)
                df_names.append(new_col_name)
    logs, raw_ans, logs_names = log_cls.return_lists()
    df_list.append(logs)
    df_list.append(raw_ans)
    df_names = df_names + logs_names
    print(df_list, df_names)
    return pd.Series(df_list, index=df_names)









'''
start = time.time()
neural_net = current_model()
new_df = input_df.apply(lambda row: iterate_one_dict(row, question_dict_dict, neural_net), axis = 1)
new_df.to_csv('C:/Users/daria/Documents/llm_cardio/medtextscan_test_simple_res.csv')

end = time.time()
print('all time',end - start)
'''


#print(new_df)

