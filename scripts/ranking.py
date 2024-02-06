#1.0 Load libraries
import pandas as pd

#2.0 Set importance of each ranking
numDocks=10
overWeight=20
obese=100
deprivation=50
cycling=1

#3.0 replace non-ranked entities with chosen values
raw_data=pd.read_csv("../assets/combinedData.csv")


#4.0 Create overall rank based on weightings
raw_data["overallScore"]=(cycling*raw_data["cyclingRank"])+(numDocks*raw_data["numDockingMSOARank"])+(overWeight*raw_data["overweightRank"])+(deprivation*raw_data["deprivationRank_mean"])+(obese*raw_data["obesityRank"])
final_dataframe=raw_data.sort_values(by='overallScore', ascending=True)
final_dataframe['overallRank'] = final_dataframe['overallScore'].rank(ascending=True,na_option='bottom',method='max',pct=False)

final_dataframe.to_csv("../assets/finalDataset.csv",index=False)
