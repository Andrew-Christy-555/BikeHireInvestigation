import requests
import json
import pandas as pd
from io import StringIO


deprivation_url="https://services3.arcgis.com/ivmBBrHfQfDnDf8Q/arcgis/rest/services/Indices_of_Multiple_Deprivation_(IMD)_2019/FeatureServer/0/query?where=1%3D1&outFields=lsoa11cd,lsoa11nm,IMD_Rank,IMD_Decile,LSOA01NM,LADcd,LADnm,IMDScore,IMDRank0,IMDDec0&returnGeometry=false&resultType=standard&outSR=&f=json"
rawDeprivationData = requests.get(deprivation_url,verify=False)
DeprivationData=rawDeprivationData.json()

deprivation_url_2="https://services3.arcgis.com/ivmBBrHfQfDnDf8Q/arcgis/rest/services/Indices_of_Multiple_Deprivation_(IMD)_2019/FeatureServer/0/query?where=1%3D1&outFields=lsoa11cd,lsoa11nm,IMD_Rank,IMD_Decile,LSOA01NM,LADcd,LADnm,IMDScore,IMDRank0,IMDDec0&returnGeometry=false&resultType=standard&outSR=&resultOffset-23000&f=json"
rawDeprivationData_2 = requests.get(deprivation_url_2,verify=False)
#rawDeprivationData=pd.json_normalize(DeprivationData)
DeprivationData_2=rawDeprivationData_2.json()

fields=["lsoa11cd","lsoa11nm","IMD_Rank","IMD_Decile","LSOA01NM","LADcd","LADnm","IMDScore","IMDRank0","IMDDec0"]

column_names=DeprivationData["fields"]
fields = [d['name'] for d in column_names]
print(fields)

combinedDeprivationData=pd.DataFrame(columns=fields)   

for i in range(0,len(DeprivationData["features"]),1):
        col_val=DeprivationData["features"][i]["attributes"]
        df_stage=pd.DataFrame(col_val,index=[0])
        combinedDeprivationData=pd.concat([combinedDeprivationData,df_stage],axis=0)   
for i in range(0,len(DeprivationData_2["features"]),1):
        col_val=DeprivationData_2["features"][i]["attributes"]
        df_stage=pd.DataFrame(col_val,index=[0])
        combinedDeprivationData=pd.concat([combinedDeprivationData,df_stage],axis=0)   

LSOAUpdated=pd.DataFrame(columns=['lsoa11cd','LSOA21CD','LSOA21NM'])
print(deprivationData)
for j in range(0,len(combinedDeprivationData),1):
    if j%1000 ==0:
        print(j)
    LSOA_11=combinedDeprivationData.iloc[j]['lsoa11cd']
    api_url="https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA11_LSOA21_LAD22_EW_LU/FeatureServer/0/query?where=F_LSOA11CD%20%3D%20'" +LSOA_11+"'&outFields=F_LSOA11CD,LSOA11NM,LSOA21CD,LSOA21NM&returnGeometry=false&outSR=4326&resultType=standard&f=json"
    updatedLSOAs = requests.get(api_url,verify=False)
    updatedLSOAs=updatedLSOAs.json()
    LSOA_Name=updatedLSOAs["features"][0]["attributes"]["LSOA21NM"]
    LSOA_Code=updatedLSOAs["features"][0]["attributes"]["LSOA21CD"]
    LSOAStage=pd.DataFrame(columns=['lsoa11cd','LSOA21CD','LSOA21NM'])
    LSOAStage.loc[0]=[LSOA_11,LSOA_Code,LSOA_Name]
    LSOAUpdated=pd.concat([LSOAUpdated,LSOAStage],axis=0)  

deprivedDataCombined=pd.merge(combinedDeprivationData,LSOAUpdated,how="left",on=["lsoa11cd"])
deprivedDataFinal=deprivedDataCombined.drop_duplicates(inplace=False)

deprivedDataFinal.to_csv("deprivation_data.csv",index=False)
