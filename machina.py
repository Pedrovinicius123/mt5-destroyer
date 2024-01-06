from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from torch import nn
import pandas as pd
import numpy as np


def make_dataframe(inp):
    arr = np.array(inp)

    dataf = pd.DataFrame(data={
        "upper": arr[0],
        "lower": arr[1],
        "result": arr[2]
    })

    print(dataf)

    return dataf


df = make_dataframe([[1, 2, 3, 4], [5, 6, 7, 8]])

pipe = make_pipeline(StandardScaler(), StratifiedKFold(), DecisionTreeClassifier())
result = pipe.fit()
