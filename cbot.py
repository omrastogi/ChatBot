from torch import nn
import torch as tf
from sublayer import  MultiHeadAttention
from word_embeding import Embedder
import config
from pytorch_lightning import LightningModule
import torch.nn.functional as F
from torch.optim import Adam


class Model(LightningModule):
    def __init__(self):
        super(Model, self).__init__()
        # self.embedder = Embedder()
        self.dropout = nn.Dropout(0.2)

        self.input_layer = nn.Sequential(
            nn.Linear(96, 64),
            nn.GELU(),
            nn.Linear(64, 48))

        self.self_attention_lg = MultiHeadAttention(heads=8, d_model=48)

        self.lg_to_md = nn.Sequential(
            nn.Linear(48, 40),
            nn.GELU(),
            nn.Linear(40, 32))

        self.self_attention_md = MultiHeadAttention(heads=8, d_model=32)

        self.feed_forward_md = nn.Sequential(
            nn.Linear(32, 64),
            nn.GELU(),
            nn.Linear(64, 32))

        self.md_to_sm = nn.Sequential(
            nn.Linear(32, 32),
            nn.GELU(),
            nn.Linear(32, config.n))

        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # x = tf.Tensor(self.embedder.generate(seq))
        x = self.input_layer(x)
        x = self.self_attention_lg(x, x, x)
        x = self.lg_to_md(x)
        x = self.dropout(x)
        x = self.self_attention_md(x, x, x)
        x = tf.mean(x, dim=1)
        x = self.md_to_sm(x)
        x = self.dropout(x)
        out = self.softmax(x)
        return out

    def total_params(self):
        return sum(p.numel() for p in self.parameters())

    def validation_step(self, batch, batch_idx):
        pat, lab = batch
        pred = self.forward(pat)
        loss = F.cross_entropy(pred.view(-1, pred.size(-1)), lab.contiguous().view(-1), ignore_index=1)
        self.log('val_loss', loss)
        return loss


    def test_step(self, batch, batch_idx):
        pat, lab = batch
        pred = self.forward(pat)
        loss = F.cross_entropy(pred.view(-1, pred.size(-1)), lab.contiguous().view(-1), ignore_index=1)
        self.log('test_loss', loss)
        return loss


    def training_step(self, batch, batch_idx):
        pat, lab = batch
        pred = self.forward(pat)
        loss = F.cross_entropy(pred.view(-1, pred.size(-1)), lab.contiguous().view(-1), ignore_index=1)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters())
        return optimizer


if __name__ == "__main__":
    model = Model()
    seq = Embedder().generate("how are you")
    print(model(seq))
    print(model.total_params())