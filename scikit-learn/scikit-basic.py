import pandas as pd


data = pd.read_csv(r"C:\Users\User\PycharmProjects\pyprojects\scikit-learn\data_files\hate_crimes.csv")
voted_trump = data[data['share_voters_voted_trump']>0.5]
not_voted_trump = data[data['share_voters_voted_trump']<0.5]
#print(f"vote trump: {voted_trump["avg_hatecrimes_per_100k_fbi"].mean} hate crime per 100K people")
#print(f"not vote trump: {not_voted_trump["avg_hatecrimes_per_100k_fbi"].mean} hate crime per 100K people")
print(voted_trump["avg_hatecrimes_per_100k_fbi"].values.mean)