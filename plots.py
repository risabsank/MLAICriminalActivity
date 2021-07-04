import plotly as py
import plotly.graph_objs as go
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
    
    query = ('''select a.YEAR, b.unemployment_rate, b.median_income, b.poverty_rate, b.county from db.onlinearrestdata1980_2019 a 
                join db.ca_county_agency_contextual_indicators_2009_2014_05_03_2016 b on a.YEAR = b.year and replace(a.COUNTY, ' County', '') = b.county
                where b.agency_name = 'All Combined'
                ''')
    
    print(query)
    start_date = 2000
    end_date = 2005
    cursor.execute(query)
    y = []
    r = []
    c = []
    black = []
    hispanic = []
    white = []
    other = []
    # with open('arrests.csv','w') as f:
    for row in cursor:
        # f.write(f'{row["YEAR"]}, {row["RACE"]}, {row["CRIMES"]}\n')
        print(f'{row["YEAR"]}, {row["RACE"]}, {row["CRIMES"]}')
        if row["YEAR"] not in y:
            y.append(row["YEAR"])
        if row["RACE"] == "Black":
            # print(type(row["CRIMES"]))
            black.append(int(row["CRIMES"]))
            # print(black)
        if row["RACE"] == "White":
            white.append(int(row["CRIMES"]))
        if row["RACE"] == "Hispanic":
            hispanic.append(int(row["CRIMES"]))
        if row["RACE"] == "Other":
            other.append(int(row["CRIMES"]))
        r.append(row["RACE"])
    print(black)
    print(y)
    print(r)
    print(c)
    percent_crimes = [100 * 20 * (x / sum(c)) for x in c]
    # print(percent_crimes)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=black, mode='lines+markers', name='black'))
    fig.add_trace(go.Scatter(x=y, y=white, mode='lines+markers', name='white'))
    fig.add_trace(go.Scatter(x=y, y=hispanic, mode='lines+markers', name='hispanic'))
    fig.add_trace(go.Scatter(x=y, y=other, mode='lines+markers', name='other'))

    # fig = go.Figure(data=[
    #     go.Bar(name="black", x=y, y=black, textposition='auto'),
    #     go.Bar(name="white", x=y, y=white, textposition='auto'),
    #     go.Bar(name="hispanic", x=y, y=hispanic, textposition='auto'),
    #     go.Bar(name="other", x=y, y=other, textposition='auto')
    # ])


    # fig = go.Figure(data=[go.Scatter(
    #     x=r, y=y,
    #     mode='markers',
    #     marker_size=percent_crimes
    #     # marker=dict(
    #     #     size=c,
    #     #     sizemode='area',
    #     #     sizeref=2.*float(max(c))/(40.**2),
    #     #     sizemin=4
    #     # )
    # )])
    # fig.update_layout(barmode='group')
    fig.show()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cnx.close()
# x = np.linspace(0, np.pi, 1000)
# layout = go.Layout(
#     title='example',
#     yaxis=dict(
#         title='volts'
#     ),
#     xaxis=dict(
#         title='nanosec'
#     )
# )

# trace1 = go.Scatter(
#     x=x,
#     y=np.sin(x),
#     mode='lines',
#     name='sin(x)',
#     line=dict(
#         shape='spline'
#     )
# )

# fig = go.Figure(data=[trace1], layout=layout)
# py.offline.iplot(fig)
