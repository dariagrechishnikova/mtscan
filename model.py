from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from transformers import GenerationConfig
import time


class current_model():
    def __init__(self):
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        self.generation_config = GenerationConfig.from_pretrained("Den4ikAI/FRED-T5-LARGE_text_qa")
        self.tokenizer = AutoTokenizer.from_pretrained("Den4ikAI/FRED-T5-LARGE_text_qa")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Den4ikAI/FRED-T5-LARGE_text_qa").to(self.device)
        self.model.eval()


    def generate(self, prompt, log_cls):
        start = time.time()
        data = self.tokenizer(f"{prompt}", return_tensors="pt").to(self.model.device)
        promt_len = len(self.tokenizer.encode(prompt))
        if promt_len > 2241:
            log_cls.write_log(message='Длина токенизированного входа > 2241, не хватает памяти', model_answer='Модель не запускалась')
            out = ''
        else:
            output_ids = self.model.generate(
                **data,
                generation_config=self.generation_config
            )[0]
            out = self.tokenizer.decode(output_ids.tolist())
        end = time.time()
        #print('model time', end - start)
        return out



