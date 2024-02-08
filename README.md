# *BikeHireInvestigation*

Project to investigate potential locations for new bike docking stations

## Documentation

**scripts**
1. **getLondonAreas.py** calls from the ONS Open Geography APIs to return all Lower Super Output Areas (LSOAs), Middle Super Output Areas (MSOAs) and Local Authority Districts (LADs) in the London region
2. **getDockingStations.py** calls the TfL BikePoint API to return the location of all bike docking stations, and appends their LSOAs, MSOAs and LADs
3. **getDeprivationData.py** calls on the Indices of Multiple Deprivation API to get deprivation data at LAD level
4. **getObesityCyclingData.py** calls on the Public Health England data API to extract obsesity, overweight and cycling to work statistics at LAD level  
5. **combineData.py** ranks the LADs and MSOAs by each parameter and then collates all of the datasets created in scripts 1-4 into a single dataset
6. **ranking.py** applies weightings to the ranks of each MSOA, to produce a final score. The current weights are placeholders, and would be agreed with policy stakeholders
7. **dataPrep.sh** is a bash script which runs all of the Python scripts to prepare the data
 
**assets**
**finalDataset.csv** is a dataset showing the Obesity, Overweight, Deprivation statistics, and the number of bike docking stations at MSOA/LAD resolution


## Code status

Currently under development


## Upcoming Development/ Next Steps

* Interactive Map within the Dashboard to show current bikepoint locations, and to show different obesity/deprivation data when users hover over a prospective new bike docking site
* Additional analysis to generate the average length of cycle hire journey, which could be used to support decisions in where to place new bike docking stations - as docking stations should be placed within a reasonable range from existing stations
* Investigate how deprivation impacts bike hire usage (would a support scheme to give free usage to those in severe deprivation significantly improve uptake?) 

## Contact

Andrew Christy - andrewchristy93@gmail.com

## License
[Creative Comms License](/LICENSE)



