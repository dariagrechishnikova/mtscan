





class log():
    def __init__(self):
        self.logs = []
        self.model_ans = []
        self.log_col_names = ['log_message', 'model_answer']


    def write_log(self, message, model_answer):
        self.logs.append(message)
        self.model_ans.append(model_answer)
        return

    def return_lists(self):
        return self.logs, self.model_ans, self.log_col_names

