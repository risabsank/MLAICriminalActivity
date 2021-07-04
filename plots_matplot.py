import plotly as py
import plotly.graph_objs as go
import ipywidgets as widgets
import numpy as np
from scipy import special
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
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

    query = ('''SELECT CASE WHEN YEAR BETWEEN 1980 AND 1990 THEN 'y 1980-90' 
    WHEN YEAR BETWEEN 1991 AND 2000 THEN 'y 1991-2000' 
    WHEN YEAR BETWEEN 2001 AND 2010 THEN 'y 2001-10' 
    WHEN YEAR BETWEEN 2011 AND 2019 THEN 'y 2011-20' end 
    YEAR, RACE, SUM(F_TOTAL + M_TOTAL + S_TOTAL) AS CRIMES FROM onlinearrestdata1980_2019 GROUP BY 1, RACE ORDER BY YEAR ASC
    ''')
    print(query)
    start_date = 2000
    end_date = 2005
    cursor.execute(query)
    y = []
    r = []
    c = []
    # with open('arrests.csv','w') as f:
    for row in cursor:
        # f.write(f'{row["YEAR"]}, {row["RACE"]}, {row["CRIMES"]}\n')
        y.append(row["YEAR"])
        r.append(row["RACE"])
        c.append(row["CRIMES"])

    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
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
