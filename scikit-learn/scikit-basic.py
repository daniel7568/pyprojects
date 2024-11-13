import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

data = pd.read_csv(r"C:\Users\User\PycharmProjects\pyprojects\scikit-learn\data_files\hate_crimes.csv")
voted_trump = DataFrame(data[])