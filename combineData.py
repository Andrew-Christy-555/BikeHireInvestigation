import pandas as pd

dockingStations=pd.read_csv("dockingStationsLSOA.csv")
dockingStationsMSOA=pd.read_csv("dockingStationsMSOA.csv")
deprivationData=pd.read_csv("deprivation_data.csv")
cyclingData=pd.read_csv("cycling_data.csv")
obesityData=pd.read_csv("obesity_data.csv")
LondonAreas=pd.read_csv("LondonAreas.csv")

dockingStationsMSOA_trimmed=dockingStationsMSOA[['MSOA21CD','Count_of_Docking_Stations']]
dockingStationsMSOA_trimmed.rename(columns={'Count_of_Docking_Stations': 'Count_of_Docking_Stations_MSOA'}, inplace=True)

#newdf=LondonAreas.join(dockingStations,how="left",on=["LSOA21CD"])
newdf=pd.merge(LondonAreas,dockingStations,how="left",on=["LSOA21CD"])
print(len(newdf))
newdf_1=pd.merge(newdf,dockingStationsMSOA_trimmed,how="left",on=["MSOA21CD"])
newdf_2=pd.merge(newdf_1,obesityData,how="left",on=["LAD22NM"])
print(len(newdf_2))
newdf_3=pd.merge(newdf_2,deprivationData,how="left",on=["LSOA21CD"])
print(len(newdf_3))
newdf_4=pd.merge(newdf_3,cyclingData,how="left",on=["LAD22NM"])
newdf_4['Count_of_Docking_Stations_MSOA'].fillna(value=0,inplace=True)
newdf_4['Count_of_Docking_Stations'].fillna(value=0,inplace=True)
newdf_4.to_csv("CombinedData.csv",index=False)
print(len(newdf))

