

def parse_one_box(input, dict_q, type_key):
    type_dict = {}
    if input is not None:
        textsplit = input.splitlines()

        for cur_str in textsplit:
            parts = cur_str.split(':')
            print('hhhhhhhhhh',parts)
            inp_questions = parts[1].split(',')
            type_dict[type_key] = inp_questions
            dict_q[parts[0]] = type_dict
    print(dict_q)




def parse_boxes(num_box, bin_box):
    dict_q = {}
    parse_one_box(input = num_box, dict_q = dict_q, type_key = 'numeric')
    parse_one_box(input= bin_box, dict_q=dict_q, type_key='binary')
    print('ddddd',dict_q)
    return dict_q


