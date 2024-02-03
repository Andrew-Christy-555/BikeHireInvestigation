import requests
import json
import pandas as pd
from io import StringIO

def output_area_lookup(output_code,output_name,ONS_boundary,input_df):
    fields=["BikeDockName",output_code,output_name]
    OA_df=pd.DataFrame(columns=fields)  
    baseUrl = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"+ONS_boundary+"/FeatureServer/0/query?where=1%3D1&outFields="+output_code+","+output_name+"&geometry="
    endUrl="&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelWithin&returnGeometry=false&outSR=4326&f=json"
    for j in range(0,len(input_df),1):
            lat=str(input_df.iat[j,2])
            lon=str(input_df.iat[j,3])
            bikeName=input_df.iat[j,4]
            full_link=baseUrl+lon+","+lat+","+lon+","+lat+endUrl
            bikeOAs = requests.get(full_link,verify=False)
            bikeOAs=bikeOAs.json()
            OA_Name=bikeOAs["features"][0]["attributes"][output_name]
            OA_Code=bikeOAs["features"][0]["attributes"][output_code]
            oa_stage=pd.DataFrame(columns=fields)
            oa_stage.loc[0]=[bikeName,OA_Code,OA_Name]
            OA_df=pd.concat([OA_df,oa_stage],axis=0)  
    return OA_df



url_id="https://api.tfl.gov.uk/BikePoint/"
bikeData = requests.get(url_id,verify=False)
extractedBikeData=bikeData.json()
bikeDataFrame=pd.DataFrame(extractedBikeData)


for col in bikeDataFrame.columns:
        print(col)
listOfStations=bikeDataFrame[["id","commonName","lat","lon","commonName"]]
print(len(listOfStations))

#print(listOfStations.head())

        

MSOALoc=output_area_lookup("MSOA21CD","MSOA21NM","MSOA_2021_EW_BGC_V2",listOfStations)
dockingStationCountsMSOA = MSOALoc.groupby(['MSOA21CD'])["MSOA21CD"].count().reset_index(name="Count_of_Docking_Stations")

dockingStationCountsMSOA.to_csv("dockingStationsMSOA.csv",index=False)

LSOALoc=output_area_lookup("LSOA21CD","LSOA21NM","Lower_layer_Super_Output_Areas_2021_EW_BGC_V3",listOfStations)
dockingStationCountsLSOA = LSOALoc.groupby(['LSOA21CD'])["LSOA21CD"].count().reset_index(name="Count_of_Docking_Stations")

dockingStationCountsLSOA.to_csv("dockingStationsLSOA.csv",index=False)

