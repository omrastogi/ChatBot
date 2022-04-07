import pandas as pd
from word_embeding import Embedder
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split


class CustomTokenLoader(DataLoader):
    """
    Returns tokenized data
    Parameter:
    df - Dataframe that contains labels and patterns
    """
    def __init__(self, df: pd.DataFrame):
        self.label = df['ids']
        self.pattern = df['patterns']
        self.embed = Embedder()

    def __len__(self):
        return len(self.label)

    def pad(self, seq):
        MAXLEN = 10

    def __getitem__(self, idx: int):
        label = self.label.iloc[idx]
        pattern = self.embed.generate(self.pattern.iloc[idx])

        return pattern, label


def get_loader():
    # read the csv data
    df = pd.read_csv("train.csv", error_bad_lines=False)
    df = df.dropna()
    # df = df.head(100)
    # split train-val dataset
    train_text, val_split = train_test_split(df,
                                             random_state=2018,
                                             test_size=0.2)

    # test-val split
    validation_text, test_text = train_test_split(val_split,
                                                  random_state=2018,
                                                  test_size=0.4)

    # Create CustomTokenLoader Object
    train_data = CustomTokenLoader(train_text)
    valid_data = CustomTokenLoader(validation_text)
    test_data = CustomTokenLoader(test_text)

    # Get dataloader
    train_dataloader = DataLoader(train_data, batch_size=1)
    valid_dataloader = DataLoader(valid_data, batch_size=1)
    test_dataloader = DataLoader(test_data, batch_size=1)

    return train_dataloader, valid_dataloader, test_dataloader


