import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

data = pd.read_csv(r"C:\Users\User\PycharmProjects\pyprojects\scikit-learn\data_files\hate_crimes.csv")
voted_trump = DataFrame(data['share_voters_voted_trump']>50])
not_voted_trump = Data[data['share_voters_voted_trump']<50]
print(f"vote trump: {voted_trump["avg_hatecrimes_per_100k_fbi"].mean} hate crime per 100K people")
print(f"not vote trump: {not_voted_trump["avg_hatecrimes_per_100k_fbi"].mean} hate crime per 100K people")