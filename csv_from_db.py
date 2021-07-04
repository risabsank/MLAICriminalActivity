from pandas.core.base import SpecificationError
import plotly as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots


import ipywidgets as widgets
import numpy as np
from scipy import special

import mysql.connector
from mysql.connector import errorcode

username = 'aiy'
pwd = 'fr3M@ntst3m'
hostname = '107.3.144.169'
portnumber = 6603
databasename = 'db'

print(errorcode.ER_ACCESS_DENIED_ERROR)
print(errorcode.ER_BAD_DB_ERROR)

# AGE_GROUP on x, 
try:
    cnx = mysql.connector.connect(user=username, password=pwd,
                                  host=hostname,
                                  port=portnumber,
                                  database=databasename)
    print("connection succeeded")

    cursor = cnx.cursor(dictionary=True)

    # query = ('''SELECT CASE WHEN YEAR BETWEEN 1980 AND 1990 THEN 'y 1980-90' 
    # WHEN YEAR BETWEEN 1991 AND 2000 THEN 'y 1991-2000' 
    # WHEN YEAR BETWEEN 2001 AND 2010 THEN 'y 2001-10' 
    # WHEN YEAR BETWEEN 2011 AND 2020 THEN 'y 2011-20' end 
    # YEAR, RACE, SUM(F_TOTAL + M_TOTAL + S_TOTAL) AS CRIMES FROM onlinearrestdata1980_2019 GROUP BY 1, RACE ORDER BY RACE, YEAR
    # ''')
    
    query = ('''select
	a.YEAR,
	a.COUNTY,
	b.Population,
	b.Median_Age,
	b.Unemployment,
	b.Income,
	sum( a.F_TOTAL + a.M_TOTAL + a.S_TOTAL ) AS crimes
from
	db.onlinearrestdata1980_2019 a
join db.datacommons_calif b on
	a.YEAR = b.year
	and a.COUNTY = b.County
where
	a.YEAR BETWEEN 2011 AND 2019
group by
	1,
	2,
	3,
	4,
	5,
	6
order by
	1,
	2,
	3,
	4,
	5,
	6
                ''')
    
    print(query)
    start_date = 2000
    end_date = 2005
    cursor.execute(query)
    with open('downloaded_data.csv','w') as f:
        f.write("Year,County,Population,Median_Age,Unemployment,MedianIncome,Crimes,CrimesBy100K,CrimeCat\n")
        for row in cursor:
            outstr = ""
            for element in row:
                outstr = f'{outstr}{row[element]},'
            crimesby100k = 100000 * (float(row["crimes"]) / float(row["Population"]))
            
            crime_cat = "Low"
            if crimesby100k > 2580:
                crime_cat = "Medium-Low"
            if crimesby100k > 3070:
                crime_cat = "Medium"
            if crimesby100k > 3611:
                crime_cat = "Medium-High"
            if crimesby100k > 4275:
                crime_cat = "High"
            
            outstr = outstr + f'{crimesby100k},{crime_cat},'
            outstr = outstr[:-1]
            f.write(f'{outstr}\n')
    


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cnx.close()
