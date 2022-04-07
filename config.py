import pandas
import pandas as pd

df = pd.read_csv("response.csv")
n = len(df)
weight_path = "checkpoints/"
epoch = 100
checkpoint = None
