#Code to extract locations of all Santander Bike Docking Stations and assign them to an LSOA and MSOA

########################
#1.0 Install libraries
import requests
import json
import pandas as pd


#############################################################################################################

#Function that will look through a dataframe, extracting the latitude and
#longitude vlues and then returning the relevant MSOAs and LSOAs using the arcGIS API
def output_area_lookup(output_code,output_name,ONS_boundary,input_df):
    #output_code = string corresponding to boundary level code e.g. LSOA21CD
    #output_name = string corresponding to boundary level name e.g. LSOA21NM
    #ONS_boundary = string corresponding to boundary map from the ONS e.g. MSOA_2021_EW_BGC_V2
    #input_df = dataframe consisting of bikePoint names and their latitudes and longitudes
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
#############################################################################################################


#2.0 Extract dataframe of all BikePoints for Santander Bikes
url_id="https://api.tfl.gov.uk/BikePoint/"
bikeData = requests.get(url_id,verify=False)
extractedBikeData=bikeData.json()
bikeDataFrame=pd.DataFrame(extractedBikeData)


for col in bikeDataFrame.columns:
        print(col)

#3.0 Create dataframe with only the relevant columns
listOfStations=bikeDataFrame[["id","commonName","lat","lon","commonName"]]
#listOfStations.to_csv('coordinates_of_bike_points.csv',index=False)

#4.0 generate dataframe for MSOAs of all the bikePoints
MSOALoc=output_area_lookup("MSOA21CD","MSOA21NM","MSOA_2021_EW_BGC_V2",listOfStations)
dockingStationCountsMSOA = MSOALoc.groupby(['MSOA21CD'])["MSOA21CD"].count().reset_index(name="Count_of_Docking_Stations")
dockingStationsMSOA_trimmed=dockingStationCountsMSOA[['MSOA21CD','Count_of_Docking_Stations']]
dockingStationsMSOA_trimmed.rename(columns={'Count_of_Docking_Stations': 'Count_of_Docking_Stations_MSOA'}, inplace=True)
dockingStationsMSOA_trimmed.drop_duplicates()
#5.0 Export the dataframe
dockingStationsMSOA_trimmed.to_csv("../assets/dockingStationsMSOA.csv",index=False)

#6.0 generate dataframe for LSOAs of all the bikePoints
LSOALoc=output_area_lookup("LSOA21CD","LSOA21NM","Lower_layer_Super_Output_Areas_2021_EW_BGC_V3",listOfStations)
dockingStationCountsLSOA = LSOALoc.groupby(['LSOA21CD'])["LSOA21CD"].count().reset_index(name="Count_of_Docking_Stations")
#7.0 Export the dataframe
dockingStationCountsLSOA.to_csv("../assets/dockingStationsLSOA.csv",index=False)

