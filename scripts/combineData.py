#1.0 load libraries
import numpy as np
import pandas as pd

#2.0 load data
dockingStations=pd.read_csv("../assets/dockingStationsLSOA.csv")
dockingStationsMSOA=pd.read_csv("../assets/dockingStationsMSOA.csv")
deprivationData=pd.read_csv("../assets/deprivation_data.csv")
cyclingData=pd.read_csv("../assets/cycling_data.csv")
obesityData=pd.read_csv("../assets/obesity_data.csv")
overweightData=pd.read_csv("../assets/overweight_data.csv")
LondonAreas=pd.read_csv("../assets/LondonAreas.csv")

#3.0 get list of Local Authority Districts
LADs=LondonAreas[["LAD22NM","LAD22CD"]].drop_duplicates()
#4.0 Get list of MSOAs
MSOAs=LondonAreas[["MSOA21NM","MSOA21CD","LAD22CD"]].drop_duplicates()
MSOA_Full_Info=LondonAreas[["LAD22NM","LAD22CD","MSOA21NM","MSOA21CD"]].drop_duplicates()

#5.0 Create dataframes with only one rwo per MSOA or LAD, depending on the source resolution
locationDockingStationsMSOA=pd.merge(MSOAs,dockingStationsMSOA,how="left",on=["MSOA21CD"])
locationObesity=pd.merge(LADs,obesityData,how="left",on=["LAD22NM"])
locationOverweight=pd.merge(LADs,overweightData,how="left",on=["LAD22NM"])
locationCycling=pd.merge(LADs,cyclingData,how="left",on=["LAD22NM"])

#6.0 Join deprivation data to all London LSOAs, as Deprivation data is at LSOA resolution
locationDeprivation=pd.merge(LondonAreas,deprivationData,how="left",on=["LSOA21CD"])
#7.0 Aggregate Deprivation data
summarisedLocationDeprivation = locationDeprivation.groupby('MSOA21CD')['IMDScore'].agg(['mean', 'median', 'max'])
summarisedLocationDeprivation.rename(columns={'mean': 'IMD mean', 'median': 'IMD median', 'max': 'IMD max'}, inplace=True)

#8.0 QA step to check for nulls and missing data

def count_empty_rows(df_name,column_name):
    empty_count = df[column_name].isnull().sum()
    populated_count = df[column_name].count()
    num_rows=len(df_name)
    return empty_count, populated_count,num_rows

all_dataframes={'Deprivation':summarisedLocationDeprivation,
        'Cycling':locationCycling,
        'Obesity':locationObesity,
        'Overweight':locationOverweight,
        'Docking':locationDockingStationsMSOA
    }
for name, df in all_dataframes.items():
    if df is summarisedLocationDeprivation:
        col_name='IMD mean'
    elif df is locationCycling:
        col_name='Cycling Percentage'
    elif df is locationObesity:
        col_name='Obesity Percentage (18+)'
    elif df is locationOverweight:
        col_name='Overweight Percentage (18+)'
    elif df is locationDockingStationsMSOA:
        col_name='Count_of_Docking_Stations_MSOA'
    empty,populated,length = count_empty_rows(df,col_name)   
    qa_max=df[col_name].max()
    qa_min=df[col_name].min()
    qa_mean=df[col_name].mean()
    qa_median=df[col_name].median()
    qa_stdev=df[col_name].stdev()
    print(name)
    print(f"Number of empty rows: {empty}")
    print(f"Number of populated rows: {populated}")
    print(f"Min Value: {qa_min}")
    print(f"Max Value: {qa_max}")
    print(f"Mean Value: {qa_mean}")
    print(f"Standard Deviation Value: {qa_stdev}")
    print(f"Median Value: {qa_median}")

#9.0 eplace nulls with 0s for MSOAs that don't have any docking stations and convert value to int
locationDockingStationsMSOA['Count_of_Docking_Stations_MSOA'].fillna(0, inplace=True)
locationCycling['Cycling Percentage'].fillna(0, inplace=True)
locationDockingStationsMSOA['Count_of_Docking_Stations_MSOA']=locationDockingStationsMSOA['Count_of_Docking_Stations_MSOA'].astype(int)

#10.0 sum number of docking stations in each local authority district
dockingStationsLADs = locationDockingStationsMSOA.groupby('LAD22CD')['Count_of_Docking_Stations_MSOA'].sum()
locationDockingStationsMSOA['Num Docking Stations Local Authority Districs']=locationDockingStationsMSOA['LAD22CD'].map(dockingStationsLADs)


#11.0 Add rankings
locationObesity['obesityRank'] = locationObesity['Obesity Percentage (18+)'].rank(ascending=False,na_option='keep',method='min',pct=False)
locationOverweight['overweightRank'] = locationOverweight['Overweight Percentage (18+)'].rank(ascending=False,na_option='keep',method='min',pct=False)
locationDockingStationsMSOA['numDockingMSOARank'] = locationDockingStationsMSOA['Count_of_Docking_Stations_MSOA'].rank(ascending=True,na_option='top',method='min',pct=False)
summarisedLocationDeprivation['deprivationRank_mean'] = summarisedLocationDeprivation['IMD mean'].rank(ascending=False,na_option='keep',method='min',pct=False)
summarisedLocationDeprivation['deprivationRank_median'] = summarisedLocationDeprivation['IMD median'].rank(ascending=False,na_option='keep',method='min',pct=False)
summarisedLocationDeprivation['deprivationRank_max'] = summarisedLocationDeprivation['IMD max'].rank(ascending=False,na_option='keep',method='min',pct=False)
locationCycling['cyclingRank'] = locationCycling['Cycling Percentage'].rank(ascending=True,na_option='keep',method='min',pct=False)

#12.0 Combine all of the data together to produce aggregated dataset
newdf=pd.merge(MSOA_Full_Info,locationDockingStationsMSOA[['numDockingMSOARank','Count_of_Docking_Stations_MSOA','Num Docking Stations Local Authority Districs','MSOA21CD']],how="left",on=["MSOA21CD"])
print(len(newdf))
newdf_1=pd.merge(newdf,locationObesity[['obesityRank','Obesity Percentage (18+)','LAD22CD']],how="left",on=["LAD22CD"])
print(len(newdf_1))
newdf_2=pd.merge(newdf_1,locationOverweight[['overweightRank','Overweight Percentage (18+)','LAD22CD']],how="left",on=["LAD22CD"])
print(len(newdf_2))
newdf_3=pd.merge(newdf_2,summarisedLocationDeprivation,how="left",on=["MSOA21CD"])
print(len(newdf_3))
newdf_4=pd.merge(newdf_3,locationCycling[['cyclingRank','Cycling Percentage','LAD22CD']],how="left",on=["LAD22CD"])

#13.0 Export dataset
newdf_4.to_csv("../assets/combinedData.csv",index=False)
print(len(newdf_4))

