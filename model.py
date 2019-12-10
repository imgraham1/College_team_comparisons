import json
import plotly
import sqlite3
import numpy as np
import pandas as pd
import plotly.graph_objs as go

global DATABASE
DATABASE = '/Users/img/Desktop/507/Final_project/college_sports.db'

years = ['2015', '2016', '2017', '2018', '2019', 'Last 5']

comparisons = ['Wins_pct', 'Offense', 'Defense', 'Recruiting']

schools_list = ['Air Force','Akron','Alabama','Appalachian State','Arizona','Arizona State','Arkansas','Arkansas State','Army','Auburn','Ball State','Baylor','Boise State','Boston College','Bowling Green State','Brigham Young','Buffalo','Central Michigan','Charlotte','Cincinnati','Clemson','Coastal Carolina','Colorado','Colorado State','Connecticut','Duke','East Carolina','Eastern Michigan','Florida','Florida Atlantic','Florida International','Florida State','Fresno State','Georgia','Georgia Southern','Georgia State','Georgia Tech','Hawaii','Houston','Idaho','Illinois','Indiana','Iowa','Iowa State','Kansas','Kansas State','Kent State','Kentucky','Liberty','Louisiana','Louisiana Tech','Louisiana-Monroe','Louisville','Marshall','Maryland','Massachusetts','Memphis','Miami (FL)','Miami (OH)','Michigan','Michigan State','Minnesota','Mississippi State','Missouri','Navy','Nebraska','Nevada','Nevada-Las Vegas','New Mexico','New Mexico State','North Carolina','North Carolina State','North Texas','Northern Illinois','Northwestern','Notre Dame','Ohio','Ohio State','Oklahoma','Oklahoma State','Old Dominion','Oregon','Oregon State','Penn State','Purdue','Rice','Rutgers','San Diego State','San Jose State','South Alabama','South Carolina','South Florida','Southern Mississippi','Stanford','Syracuse','Temple','Tennessee','Texas','Texas A&M','Texas Christian','Texas State','Texas Tech','Toledo','Troy','Tulane','Tulsa','UCLA','Utah','Utah State','Vanderbilt','Virginia','Virginia Tech','Wake Forest','Washington','Washington State','West Virginia','Western Kentucky','Western Michigan','Wisconsin','Wyoming']

states = ['Hawaii', 'Florida', 'Oklahoma', 'Louisiana', 'Washington', 'Illinois', 'Massachusetts', 'California', 'Alabama', 'Iowa', 'New York', 'Tennessee', 'Connecticut', 'Oregon', 'Mississippi', 'Wyoming', 'Nebraska', 'Missouri', 'Georgia', 'North Carolina', 'Virginia', 'South Carolina', 'Pennsylvania', 'Arizona', 'Maryland', 'Minnesota', 'Colorado', 'Nevada', 'Idaho', 'Kentucky', 'West Virginia', 'Michigan', 'Kansas', 'New Jersey', 'Texas', 'Wisconsin', 'New Mexico', 'Indiana', 'Utah', 'Arkansas', 'Ohio']

def get_locations(column ='null'):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select "+column+" from locations")
    response = cur.fetchall()
    return response

def search_by_school(name = 'Air Force',  year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"

    if compare == "Wins_pct":
        bball = "bball_win_pct"
        fball = "fball_win_pct"
    if compare == "Offense":
        bball = "bball_ortg"
        fball = "fball_ortg"
    if compare == "Defense":
        bball = "bball_drtg"
        fball = "fball_drtg"
    if compare == "Recruiting":
        bball = "bball_recruiting"
        fball = "fball_recruiting"

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select "+bball+", "+fball+", "+compare+" from " +year+ " where School = '" + name + "'")
    response = cur.fetchall()
    return response

def get_pic(name = 'Air Force'):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select logo from pics where School = '" + name + "'")
    response = cur.fetchall()
    return response


def search_by_state1(state = 'Hawaii',  year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select " + compare + ", count(*) from " + year + " join locations on " + year + ".School = locations.School where state = '" + state + "' group by "+compare)
    response = cur.fetchall()
    return response

def search_by_state2(state = 'Hawaii',  year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"

    # select fifteen.School, Wins_pct, state from fifteen join locations on fifteen.School = locations.School where state="Michigan"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select " + year + ".School, "+compare+", state from " + year + " join locations on " + year + ".School = locations.School where state = '" + state + "'")
    response = cur.fetchall()
    return response

def search_by_state3(state = 'Hawaii',  year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"

    # select fifteen.School, Wins_pct, state from fifteen join locations on fifteen.School = locations.School where state="Michigan"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select count(*) from " + year + " join locations on " + year + ".School = locations.School where state = '" + state + "'")
    response = cur.fetchall()
    return response



def overview_search(year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"


    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select locations.School, "+compare+" from " + year + " join locations on " + year + ".School = locations.School")
    response = cur.fetchall()
    return response


def overview_search1(year = '2015', compare ='Wins_pct'):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"



    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select "+compare+", count(*) from " + year + " join locations on " + year + ".School = locations.School group by "+compare)
    response = cur.fetchall()
    return response

def graph_basketball(year="2015", compare="Wins_pct"):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"


    # DATABASE = '/Users/img/Desktop/507/Final_project/college_sports.db'
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select "+compare+", count(*) as count, abbr from "+year+" join locations on "+year+".School = locations.School where Wins_pct='Basketball' group by State")
    response = cur.fetchall()
    count = []
    abbreviation = []
    for x in response:
        count.append(x[1])
        abbreviation.append(x[2])


    cur.execute("select "+compare+", count(*) as count, abbr from "+year+" join locations on "+year+".School = locations.School where Wins_pct='Football' group by State")
    response1 = cur.fetchall()

    count1 = []
    abbreviation1 = []


    for x in response1:
        count1.append(x[1])
        abbreviation1.append(x[2])

    qdf = pd.DataFrame(list(zip(count, abbreviation, count1, abbreviation1)), columns =['count-bball', 'abbreviation-bball', 'count-fball', 'abbreviation-fball'])


    color = []

    i=0

    for x in qdf['count-bball']:
        if x > qdf['count-fball'][i]:
            color.append(100)
        else:
            color.append(50)
        i+=1

    qdf['shades']=color






    fig=go.Choropleth(
        locations=qdf['abbreviation-bball'], # Spatial coordinates
        z = qdf['shades'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        showscale = False,
        marker_line_color='gray',
        hovertext=qdf['abbreviation-bball'],
        hoverinfo="text",
    )
    # layout = go.layout.Geo(
    #     scope='usa',
    #     projection = go.layout.geo.Projection(type = 'albers usa'),
    # )
    # geo = go.layout.Geo(
    #     scope = 'usa',
    #     projection = go.layout.geo.Projection(type = 'albers usa'),
    #     showlakes = True,
    #     lakecolor = 'rgb(255, 255, 255)')
    data=[fig]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# def graph_football(year="2015", compare="Wins_pct"):
#     if year == '2015':
#         year = 'fifteen'
#     if year == '2016':
#         year = 'sixteen'
#     if year == '2017':
#         year = 'seventeen'
#     if year == '2018':
#         year = 'eighteen'
#     if year == '2019':
#         year = 'nineteen'
#     if year == "Last 5":
#         year = "totals"
#
#     # DATABASE = '/Users/img/Desktop/507/Final_project/college_sports.db'
#     conn = sqlite3.connect(DATABASE)
#     cur = conn.cursor()
#     cur.execute("select "+compare+", count(*) as count, abbr from "+year+" join locations on "+year+".School = locations.School where Wins_pct='Football' group by State")
#     response = cur.fetchall()
#     count = []
#     abbreviation = []
#     for x in response:
#         count.append(x[1])
#         abbreviation.append(x[2])
#     qdf = pd.DataFrame(list(zip(count, abbreviation)), columns =['count', 'abbreviation'])
#
#     fig=go.Choropleth(
#         locations=qdf['abbreviation'],
#         z = qdf['count'],
#         locationmode = 'USA-states',
#         colorscale = 'Blues',
#         colorbar_title = "Number of schools",
#         marker_line_color='gray',
#     )
#     data=[fig]
#
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
#
#
def graph_states(year="2015", compare="Wins_pct", state="Hawaii"):
    if year == '2015':
        year = 'fifteen'
    if year == '2016':
        year = 'sixteen'
    if year == '2017':
        year = 'seventeen'
    if year == '2018':
        year = 'eighteen'
    if year == '2019':
        year = 'nineteen'
    if year == "Last 5":
        year = "totals"

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("select "+year+".School, "+compare+", latitude, longitude from "+year+" join locations on "+year+".School = locations.School where state='"+state+"'")
    response = cur.fetchall()
    lats = []
    lons = []
    school = []
    outcome = []
    for x in response:
        school.append(x[0])
        lats.append(x[2])
        lons.append(x[3])
        outcome.append(x[1])
    color=[]
    for x in outcome:
        if x=="Basketball":
            color.append("Red")
        else:
            color.append("Blue")
    qdf = pd.DataFrame(list(zip(lats, lons, school, color)), columns =['lat', 'lon', 'school', 'color'])

    fig = go.Scattergeo(
        lat = qdf['lat'],
        lon = qdf['lon'],
        text = qdf['school'],
        mode = 'markers',
        locationmode = 'USA-states',
        marker_color = qdf['color'],
        )
    data=[fig]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

















 # end
