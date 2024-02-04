#Code to extract Cycling and Obesity Data from the Public Health England Fingertips API
#

##############################
#1.0 Load Libraries
import fingertips_py as ftp
##############################


#2.0 Extract data on the % of population over 18+ that are obese in each LAD
health_url="https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93881"
obesity_data=ftp.api_calls.deal_with_url_error(health_url)
#3.0 Subset the data for the values of interest
obesity_data=obesity_data[['Area Code','Area Name','Value','Time period']]
#4.0 Rename the columns
obesity_data.rename(columns={'Area Name': 'LAD22NM','Value':'Obesity Percentage (18+)'}, inplace=True)
#5.0 Select the most recent data
latest_obesity_data=obesity_data.loc[obesity_data['Time period']=="2021/22"]
#6.0 Export the dataset
latest_obesity_data=latest_obesity_data[['LAD22NM','Obesity Percentage (18+)']]
latest_obesity_data.to_csv("obesity_data.csv",index=False)


#7.0 Extract data on the % of adults cycling for travel at least three days per week
cycling_url="https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93440"
cycling_data=ftp.api_calls.deal_with_url_error(cycling_url)
#8.0 Subset the data for the values of interest
cycling_data=cycling_data[['Area Code','Area Name','Value','Time period']]
#9.0 create new column showing the year the data was taken
cycling_data=cycling_data.assign(DateMeasure=cycling_data["Time period"].str[:4])
#10.0 Select the most recent data
cycling_data_trimmed=cycling_data.sort_values("DateMeasure").groupby("Area Code").tail(1)
cycling_data_trimmed.rename(columns={'Area Name': 'LAD22NM','Value':'Cycling Percentage'}, inplace=True)
#11.0 Export the dataset
cycling_data_trimmed=cycling_data_trimmed[['LAD22NM','Cycling Percentage']]
cycling_data_trimmed.to_csv("cycling_data.csv",index=False)

#12.0 Extract data on the % of population over 18+ that are obese in each LAD
overweight_url="https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93088"
overweight_data=ftp.api_calls.deal_with_url_error(overweight_url)
#13.0 Subset the data for the values of interest
overweight_data=overweight_data[['Area Code','Area Name','Value','Time period']]
#14.0 Rename the columns
overweight_data.rename(columns={'Area Name': 'LAD22NM','Value':'Overweight Percentage (18+)'}, inplace=True)
#15.0 Select the most recent data
latest_overweight_data=overweight_data.loc[overweight_data['Time period']=="2021/22"]
print(latest_overweight_data.head())
latest_overweight_data=latest_overweight_data[['LAD22NM','Overweight Percentage (18+)']]
#16.0 Export the dataset
latest_overweight_data.to_csv("overweight_data.csv",index=False)

