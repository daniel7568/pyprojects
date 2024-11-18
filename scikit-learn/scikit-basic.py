import pandas as pd
from pandas.io.sas.sas_constants import column_data_length_offset
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

data = pd.read_csv(r"data_files/hate_crimes.csv")
voted_trump = data[data['share_voters_voted_trump']>0.5]
not_voted_trump = data[data['share_voters_voted_trump']<0.5]

filter_data = data.dropna()
y = filter_data["avg_hatecrimes_per_100k_fbi"]
X = filter_data.drop(columns = ["avg_hatecrimes_per_100k_fbi","hate_crimes_per_100k_splc","state",])

print(X.head())
print(y.head())
print(Pipeline.__doc__)

pipe = Pipeline([
    LinearRegression()
])

model = LinearRegression()
pipe.fit(X,y)
print(model.score(X, y))