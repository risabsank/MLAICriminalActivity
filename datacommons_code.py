import datacommons_pandas as dc

fh = open("datacommonsdata_3.csv", "w")
fh.write("Year,geoId,County,Population,Median_Age,Unemployment,Income,Crimes\n")
cal = "geoId/06"
counties = dc.get_places_in([cal], "County")
print(counties)
for county in counties["geoId/06"]:
    countyval = dc.get_property_values([county], "name")
    countyname = countyval[county][0]
    for year in range(1980, 2020):
        population = dc.get_stat_value(county, "Count_Person", date=year)
        unempl = dc.get_stat_value(county, "UnemploymentRate_Person", date=year)
        income = dc.get_stat_value(county, "Median_Income_Household", date=year)
        medianage = dc.get_stat_value(county, "Median_Age_Person", date=year)
        crimerate = dc.get_stat_value(county, "Count_CriminalActivities_CombinedCrime", date=year)


        fh.write(f'{year},{county},{countyname},{population},{medianage},{unempl},{income},{crimerate}\n')
