#Code to find all of the MSOAs and LSOAs in London


###########################
#1.0 Import Libraries
import requests
import json
import pandas as pd

#2.0 Retrieve list of all Local Authority Districts within the London Region
LondonLADs_url="https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD21_RGN21_EN_LU_e39114ca0d934551b012bba304cdd11f/FeatureServer/0/query?where=RGN21NM%20%3D%20'LONDON'&outFields=LAD21CD,LAD21NM,RGN21NM&returnGeometry=false&outSR=4326&f=json"
LADs = requests.get(LondonLADs_url,verify=False)
LADs=LADs.json()
LADlist=[]
for i in range(0,len(LADs["features"]),1):
        newLAD=LADs["features"][i]["attributes"]['LAD21CD']
        LADlist.append(newLAD)  

#3.0 Get all MSOAs and LSOAs within the LADs listed above

apiListLADs="https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/OA_LSOA_MSOA_EW_DEC_2021_LU_v3/FeatureServer/0/query?where=%20(LAD22CD%20%3D%20'"
apiListLADsEnd="&outFields=LSOA21CD,LSOA21NM,MSOA21CD,MSOA21NM,LAD22NM&returnGeometry=false&outSR=4326&resultType=standard&f=json"
#loop through Local Autority Districts, to generate API that will only select relevant LADs
for i in range(0,len(LADlist),1):
    if i < (len(LADlist)-1):
        apiListLADs = apiListLADs+LADlist[i]+"'%20OR%20LAD22CD%20%3D%20'"
    else:
        apiListLADs = apiListLADs+LADlist[i] +"')%20"
                                
apiListLADs=apiListLADs+apiListLADsEnd 
LondonOAs = requests.get(apiListLADs,verify=False)
LondonOAs=LondonOAs.json()
#Loop through all of the LSOA and MSOA instances 
# and combine them to generate a datatable of LADs, MSOAs and LSOAs
fields=["LAD22NM","MSOA21NM","MSOA21CD","LSOA21NM","LSOA21CD"]
LondonOAsList=pd.DataFrame(columns=fields)
for j in range(0,len(LondonOAs["features"]),1):
        MSOA_Name=LondonOAs["features"][j]["attributes"]["MSOA21NM"]
        MSOA_Code=LondonOAs["features"][j]["attributes"]["MSOA21CD"]
        LSOA_Name=LondonOAs["features"][j]["attributes"]["LSOA21NM"]
        LSOA_Code=LondonOAs["features"][j]["attributes"]["LSOA21CD"]
        LAD_Name=LondonOAs["features"][j]["attributes"]["LAD22NM"]
        msoa_stage=pd.DataFrame(columns=fields)
        msoa_stage.loc[0]=[LAD_Name,MSOA_Name,MSOA_Code,LSOA_Name,LSOA_Code]
        LondonOAsList=pd.concat([LondonOAsList,msoa_stage],axis=0)   

LondonOAsList.drop_duplicates(inplace=True)
LondonOAsList.to_csv("LondonAreas.csv",index=False)

    
