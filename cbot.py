import torch
import os
import time
import pandas as pd
from transformers import AutoModel, BertTokenizerFast


class Pattern_Search:
    def __init__(self, model_path="google/bert_uncased_L-6_H-256_A-4"):
        self.df = None
        self.device = None
        self.repr = None
        self.entries = None
        self.representation = None
        self.model = AutoModel.from_pretrained(model_path)
        self.tokenizer = BertTokenizerFast.from_pretrained(model_path)

    def build_representation(self, df, batch_size=1000):
        self.df = df
        self.entries = list(df["Question"].astype(str))
        l = len(self.entries)
        for i in range(0, l, batch_size):
            repr = self.get_embeddings(self.entries[i:i + batch_size], self.tokenizer, self.model, self.device)
            ques = list(self.df["Question"][i:i + batch_size])
            answ = list(self.df["Answer"][i:i + batch_size])
            newdf = pd.DataFrame({'question':ques, 'answer':answ, 'token':repr.detach().tolist()})
            if i==0:
                newdf.to_csv("data/buffer.csv", mode='w', index=False)
            else:
                newdf.to_csv("data/buffer.csv", mode='a', index=False, header=False)

        newdf = pd.read_csv("data/buffer.csv")
        newdf["token"] = pd.Series(newdf["token"].apply(eval).to_list())
        newdf.to_parquet('data/cbot.parquet.gzip', compression='gzip')
        os.remove("data/buffer.csv")

    def load_representations(self, pq_file='data/cbot.parquet.gzip'):
        S = time.time()
        self.df = pd.read_parquet(pq_file)
        self.repr = torch.Tensor(self.df['token']).type(torch.float16)

    def infer(self, inp):
        enc = self.get_embeddings(inp, self.tokenizer, self.model, self.device).type(torch.float16)
        cos_sm = self.batch_cosine_similarity(enc, self.repr)

        ans = self.df.iloc[int(torch.argmax(cos_sm))]['answer']
        score = float(torch.max(cos_sm))
        return ans, score

    @staticmethod
    def batch_cosine_similarity(inp1, inp2):
        dot_prd = torch.matmul(inp1, inp2.transpose(0, 1))
        sum1 = torch.unsqueeze(torch.sum(inp1 ** 2, dim=1), 1) ** 0.5
        sum2 = torch.unsqueeze(torch.sum(inp2 ** 2, dim=1), 1) ** 0.5
        dot_prd = torch.div(dot_prd, sum1)
        dot_prd = torch.div(dot_prd, sum2.transpose(0, 1))
        return dot_prd

    @staticmethod
    def get_embeddings(src, tokenizer, model, device):
        token = tokenizer(src, return_token_type_ids=False, padding=True, return_tensors="pt")
        ids, mask = token['input_ids'], token['attention_mask']
        if ids.shape[1] > 512: 
            ids, mask = ids[:, :500], mask[:, :500]
        with torch.no_grad():
            _, x = model(input_ids=ids, attention_mask=mask, return_dict=False)
        return x


if __name__ == "__main__":
    obj = Pattern_Search()
    obj.load_representations()
    print(obj.infer("Where is AI"))
