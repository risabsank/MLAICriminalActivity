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
	(a.COUNTY = 'Orange County'
		or a.COUNTY = 'Los Angeles County'
		or a.COUNTY = 'San Diego County'
		or a.COUNTY = 'Riverside County'
		or a.COUNTY = 'Santa Clara County'
		or a.COUNTY = 'Alameda County')
	and a.YEAR BETWEEN 2011 AND 2019
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
    y = []
    r = []
    c = []
    Orange = []
    Orange.append(list())
    Orange.append(list())
    Riverside = []
    Riverside.append(list())
    Riverside.append(list())
    Alameda = []
    Alameda.append(list())
    Alameda.append(list())
    LosAngeles = []
    LosAngeles.append(list())
    LosAngeles.append(list())
    SanDiego = []
    SanDiego.append(list())
    SanDiego.append(list())
    SantaClara = []
    SantaClara.append(list())
    SantaClara.append(list())
    # with open('arrests.csv','w') as f:
    for row in cursor:
        # f.write(f'{row["YEAR"]}, {row["RACE"]}, {row["CRIMES"]}\n')
        if row["YEAR"] not in y:
            y.append(row["YEAR"])
        if row["COUNTY"] == "Orange County":
            Orange[0].append(float(row["Population"]))
            Orange[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
        if row["COUNTY"] == "Riverside County":
            Riverside[0].append(float(row["Population"]))
            Riverside[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
        if row["COUNTY"] == "Alameda County":
            Alameda[0].append(float(row["Population"]))
            Alameda[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
        if row["COUNTY"] == "Los Angeles County":
            LosAngeles[0].append(float(row["Population"]))
            LosAngeles[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
        if row["COUNTY"] == "San Diego County":
            SanDiego[0].append(float(row["Population"]))
            SanDiego[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
        if row["COUNTY"] == "Santa Clara County":
            SantaClara[0].append(float(row["Population"]))
            SantaClara[1].append(100000 * (float(row["crimes"]) / float(row["Population"])))
    print(y)
    print(Orange)
    print(Alameda)
    print(Riverside)
    print(SanDiego)
    print(SantaClara)
    print(LosAngeles)
    percent_crimes = [100 * 20 * (x / sum(c)) for x in c]
    # print(percent_crimes)

    # fig = make_subplots(rows=2, cols=3,
    #                     specs=[[{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}],
    #                             [{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}]])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=y,y=SanDiego[1], name="Crimes"), secondary_y=False)
    fig.add_trace(go.Scatter(x=y,y=SanDiego[0], name="Population"), secondary_y=True)
    fig.update_layout(title_text="San Diego County Crimes per 100K and Population")
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Crimes (Per 100K)", secondary_y=False)
    fig.update_yaxes(title_text="Population", secondary_y=True)


    # fig.add_trace(go.Scatter(x=y, y=Orange[1], name="Crimes"), row=1, col=1, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=Orange[0], name="Population"), row=1, col=1, secondary_y=True)

    # fig.add_trace(go.Scatter(x=y, y=Riverside[1], name="Crimes"), row=1, col=2, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=Riverside[0], name="Population"), row=1, col=2, secondary_y=True)

    # fig.add_trace(go.Scatter(x=y, y=Alameda[1], name="Crimes"), row=1, col=3, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=Alameda[0], name="Population"), row=1, col=3, secondary_y=True)

    # fig.add_trace(go.Scatter(x=y, y=LosAngeles[1], name="Crimes"), row=2, col=1, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=LosAngeles[0], name="Population"), row=2, col=1, secondary_y=True)

    # fig.add_trace(go.Scatter(x=y, y=SanDiego[1], name="Crimes"), row=2, col=2, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=SanDiego[0], name="Population"), row=2, col=2, secondary_y=True)

    # fig.add_trace(go.Scatter(x=y, y=SantaClara[1], name="Crimes"), row=2, col=3, secondary_y=False)
    # fig.add_trace(go.Scatter(x=y, y=SantaClara[0], name="Population"), row=2, col=3, secondary_y=True)


    # fig.update_xaxes(title_text="Orange County", row=1, col=1)
    # fig.update_xaxes(title_text="Riverside County", row=1, col=2)
    # fig.update_xaxes(title_text="Alameda County", row=1, col=3)
    # fig.update_xaxes(title_text="Los Angeles County", row=2, col=1)
    # fig.update_xaxes(title_text="San Diego County", row=2, col=2)
    # fig.update_xaxes(title_text="Santa Clara County", row=2, col=3)



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
