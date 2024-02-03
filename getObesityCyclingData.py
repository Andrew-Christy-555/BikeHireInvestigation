import fingertips_py as ftp
import requests
#health_url='https://fingertips.phe.org.uk/api/profile?profile_id=32'

#health_url='https://fingertips.phe.org.uk/api/latest_data/specific_indicators_for_single_area?area_type_id=MSOA&area_code=E02000001&indicator_ids=93881'
health_url="https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93881"
obesity_data=ftp.api_calls.deal_with_url_error(health_url)
obesity_data=obesity_data[['Area Code','Area Name','Value','Time period']]
obesity_data.rename(columns={'Area Name': 'LAD22NM','Value':'Obesity Percentage (18+)'}, inplace=True)
latest_obesity_data=obesity_data.loc[obesity_data['Time period']=="2021/22"]
latest_obesity_data.to_csv("obesity_data.csv",index=False)


cycling_data = ftp.get_data_for_indicator_at_all_available_geographies(93440)

cycling_url="https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93440"
cycling_data=ftp.api_calls.deal_with_url_error(cycling_url)

cycling_data=cycling_data[['Area Code','Area Name','Value','Time period']]
cycling_data=cycling_data.assign(DateMeasure=cycling_data["Time period"].str[:4])
cycling_data_trimmed=cycling_data.sort_values("DateMeasure").groupby("Area Code").tail(1)
cycling_data_trimmed.rename(columns={'Area Name': 'LAD22NM','Value':'Cycling Percentage'}, inplace=True)
cycling_data_trimmed.to_csv("cycling_data.csv",index=False)


