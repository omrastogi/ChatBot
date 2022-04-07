import en_core_web_md
import torch


class Embedder:
    def __init__(self):
        self.tokenizer = en_core_web_md.load()

    def generate(self, seq):
        tensor = self.tokenizer(seq).to_dict()['tensor']
        return torch.Tensor(tensor[None, :, :])


if __name__ == "__main__":
    obj = Embedder()
    print(obj.generate(seq="Hi how are you"))




