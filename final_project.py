import re
import sqlite3
import requests
import pandas as pd
from secrets import *
# from tqdm import tqdm
from bs4 import BeautifulSoup
from opencage.geocoder import OpenCageGeocode

Ortg = []
Drtg = []
team = []
logos = []
Ortg1 = []
Drtg1 = []
links = []
years = []
teams = []
win_pct = []
len_list = [351, 351, 351, 351, 353]

year = 2015
for length in len_list:
    url = "https://www.sports-reference.com/cbb/"
    url_end1 = "seasons/"+str(year)+"-school-stats.html"
    html = requests.get(url + url_end1).text
    soup = BeautifulSoup(html, 'html.parser')

    searching_div = soup.findAll("td")

    num = 4
    for x in (range(length)):
        team.append(str(year)+searching_div[num-4].text)
        win_pct.append(searching_div[num].text)
        years.append(year)
        num+=33

    year+=1

    hrefs = soup.findAll("tbody")
    x = hrefs[0].findAll("a", href=True)
    for g in x:
        links.append(g['href'])

print("Completed initial cbb data scrape")
for x in team:
    if x.endswith("NCAA", -4):
        x = x[:-5]
        teams.append(x)
    else:
        teams.append(x)

basketball_df = pd.DataFrame(list(zip(teams, years, win_pct)), columns =['Team', 'Year', 'Bball_win_pct'])

basketball_df = basketball_df.set_index(basketball_df["Team"])

for x in links:
    url = "https://www.sports-reference.com"
    new_url = url + x
    html = requests.get(new_url).text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.findAll("img", class_="teamlogo")
    logos.append(links[0]["src"])

    searching_div = soup.findAll("p")

    o = searching_div[8].text
    d = searching_div[9].text

    o = re.search('\(([^)]+)', o).group(1)
    d = re.search('\(([^)]+)', d).group(1)

    Ortg.append(o)
    Drtg.append(d)
print("Completed cbb crawl")

basketball_df["Bball_ortg"] = Ortg
basketball_df["Bball_drtg"] = Drtg
basketball_df["logos"] = logos
basketball_df = basketball_df.set_index(basketball_df["Team"])


years = []
team = []
links = []
conf = []
teams = []
win_pct = []
len_list = [128, 128, 130, 130, 130]

year = 2015

for length in len_list:
    url = "https://www.sports-reference.com/cfb/years/"+str(year)+"-standings.html"

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    searching_div = soup.findAll("td")

    num = 0
    for x in range(length):
        team.append(str(year)+searching_div[num].text)
        conf.append(searching_div[num+1].text)
        win_pct.append(searching_div[num+4].text)
        years.append(year)
        num+=16

    year+=1

    hrefs = soup.findAll("tbody")
    x = hrefs[0].findAll("a", href=True)
    for g in x:
        links.append(g['href'])

print("Completed initial cfb data scrape")


for x in team:
    if x.endswith("NCAA", -4):
        x = x[:-5]
        teams.append(x)
    else:
        teams.append(x)

football_df = pd.DataFrame(list(zip(teams, conf, years, win_pct)), columns =['Team', 'Conf', "Year",'Fball_win_pct'])

football_df = football_df.set_index(football_df["Team"])

global links2
links2 = []
for x in links:
    if x.startswith("/cfb/schools"):
        links2.append(x)

Ortg = []
Drtg = []


for x in links2:
    url = "https://www.sports-reference.com"
    new_url = url + x
    html = requests.get(new_url).text
    soup = BeautifulSoup(html, 'html.parser')

    searching_div = soup.findAll("p")

    o = searching_div[8].text
    d = searching_div[10].text

    if o.startswith("Points/G:"):
        try:
            o = re.search('\(([^)]+)', o).group(1)
            d = re.search('\(([^)]+)', d).group(1)
        except:
            o = "none"
            d = "none"

        Ortg.append(o)
        Drtg.append(d)

    else:
        o = searching_div[7].text
        d = searching_div[9].text
        try:
            o = re.search('\(([^)]+)', o).group(1)
            d = re.search('\(([^)]+)', d).group(1)
        except:
            o = "none"
            d = "none"

        Ortg.append(o)
        Drtg.append(d)

print("Completed cfb crawl")

football_df["Fball_ortg"] = Ortg
football_df["Fball_drtg"] = Drtg


new_conf = []
for x in football_df["Conf"]:

    result = re.sub("[\(\[].*?[\)\]]", "", x)
    result = result[:-1]
    new_conf.append(result)

football_df["Conf"] = new_conf

#4 pages of this to scrape
ranking = []
recruiting_team = []

year = ["2015","2016","2017","2018","2019"]
page_number = ["1","2","3","4"]
for x in year:
    for page in page_number:
        url = "https://247sports.com/Season/"+str(x)+"-Basketball/CompositeTeamRankings/?ViewPath=~%2FViews%2FSkyNet%2FInstitutionRanking%2F_SimpleSetForSeason.ascx&Page="+str(page)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}
        html = requests.get(url,headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')


        searching_div = soup.findAll("div", class_="primary")
        for y in searching_div:
            ranking.append(str(x) + y.text)

        please = soup.findAll("a", class_="rankings-page__name-link")
        for z in please:
            recruiting_team.append(str(x) + z.text)

print("Completed cbb recruiting data scrape")



rankings1 = []
recruiting15 = []
recruiting16 = []
recruiting17 = []
recruiting18 = []
recruiting19 = []

for x in recruiting_team:
    if x.startswith("2015"):
        recruiting15.append(x)
    if x.startswith("2016"):
        recruiting16.append(x)
    if x.startswith("2017"):
        recruiting17.append(x)
    if x.startswith("2018"):
        recruiting18.append(x)
    if x.startswith("2019"):
        recruiting19.append(x)

test15 = list(range(1,154))
newtest15 = list(range(155,201))

test19 = list(range(1,103))
newtest19 = list(range(104,189))

seq1 = test15+newtest15
seq2 = list(range(1,197))
seq3 = list(range(1,196))
seq4 = list(range(1,184))
seq5 = test19 + newtest19
rankings1 = seq1+seq2+seq3+seq4+seq5

recruiting_team1=[]
for x in recruiting_team:
    recruiting_team1.append(x[:-1])



my_dict = {}
i = 0
for x in recruiting_team1:
    my_dict[x] = rankings1[i]
    i+=1

basketball_df["Bball_recruiting"] = "Nan"

i=0
test = []
for x in basketball_df["Team"]:
    if x in my_dict.keys():
        test.append(i)
        basketball_df["Bball_recruiting"][str(x)] = my_dict[str(x)]
        i+=1
    else:
        basketball_df["Bball_recruiting"][str(x)] = 200

#6 pages of this to scrape
ranking = []
recruiting_team = []

year = ["2015","2016","2017","2018","2019"]
page_number = ["1","2","3","4","5","6"]



for x in year:
    for page in page_number:
        url = "https://247sports.com/Season/"+str(x)+"-Football/CompositeTeamRankings/?ViewPath=~%2FViews%2FSkyNet%2FInstitutionRanking%2F_SimpleSetForSeason.ascx&Page="+str(page)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': user_agent}
        html = requests.get(url,headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        searching_div = soup.findAll("div", class_="primary")
        for y in searching_div:
            ranking.append(str(x) + y.text)

        please = soup.findAll("a", class_="rankings-page__name-link")
        for z in please:
            recruiting_team.append(str(x) + z.text)

print("Completed cfb recruiting data scrape")



rankings1 = []
recruiting15 = []
recruiting16 = []
recruiting17 = []
recruiting18 = []
recruiting19 = []

for x in recruiting_team:
    if x.startswith("2015"):
        recruiting15.append(x)
    if x.startswith("2016"):
        recruiting16.append(x)
    if x.startswith("2017"):
        recruiting17.append(x)
    if x.startswith("2018"):
        recruiting18.append(x)
    if x.startswith("2019"):
        recruiting19.append(x)

seq1 = list(range(1,245))
seq2 = list(range(1,247))
seq3 = list(range(1,248))
seq4 = list(range(1,233))
seq5 = list(range(1,225))
rankings1 = seq1+seq2+seq3+seq4+seq5

recruiting_team1=[]
for x in recruiting_team:
    recruiting_team1.append(x[:-1])

my_dict = {}
i = 0
for x in recruiting_team1:
    my_dict[x] = rankings1[i]
    i+=1


football_df["Fball_recruiting"] = "Nan"

i=0
test = []
for x in football_df["Team"]:
    if x in my_dict.keys():
        test.append(i)
        football_df["Fball_recruiting"][str(x)] = my_dict[str(x)]
        i+=1
    else:
        football_df["Fball_recruiting"][str(x)] = 250

new = pd.merge(basketball_df, football_df, left_index=True, right_index=True)

total_df = new.loc[:, ['Team_x','Conf','Year_x','Bball_win_pct', 'Bball_ortg', 'Bball_drtg','Bball_recruiting','Fball_win_pct', 'Fball_ortg', 'Fball_drtg', 'Fball_recruiting']].copy()

i = 0
for x in total_df["Bball_ortg"]:
    total_df["Bball_ortg"][i] = x[:-9]
    i+=1

i = 0
for x in total_df["Bball_drtg"]:
    total_df["Bball_drtg"][i] = x[:-9]
    i+=1

i = 0
for x in total_df["Fball_ortg"]:
    total_df["Fball_ortg"][i] = x[:-9]
    i+=1

i = 0
for x in total_df["Fball_drtg"]:
    total_df["Fball_drtg"][i] = x[:-9]
    i+=1

total_df.rename(columns = {'Team_x':'Team', 'Year_x':'Year'}, inplace = True)




team_names = []
for x in total_df["Team"]:
    team_names.append(x[4:])
schools = list(set(team_names))

schools[77] = "louisiana-lafayette"
schools1 =[]
for x in schools:
    x = x.lower()
    x = x.replace(" ","-")
    x = x.replace("&","")
    x = x.replace("(","")
    x = x.replace(")","")
    schools1.append(x)

locations = {}
i = 0

for x in schools1:
    url = "https://www.sports-reference.com/cfb/schools/"+x
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    searching_div = soup.findAll("p")

    o = searching_div[6].text

    if o.startswith("Location:"):
        o = o[:-1]
        locations[schools[i]] = o[11:]

    if o.startswith("Stadium:"):
        s = searching_div[7].text
        s = s[:-1]
        locations[schools[i]] = s[11:]

    if o.startswith("Ranked"):
        n = searching_div[8].text
        n = n[:-1]
        locations[schools[i]] = n[11:]

    if o.startswith("Bowl"):
        w = searching_div[9].text
        w = w[:-1]
        locations[schools[i]] = w[11:]

    if o.startswith("Conf."):
        t = searching_div[10].text
        t = t[:-1]
        locations[schools[i]] = t[11:]

    i+=1

print("Completed location crawl")

locations['Louisiana'] = locations['louisiana-lafayette']
del locations['louisiana-lafayette']

locations["Air Force"] = "Colorado Springs, Colorado"

total_df["Location"] = "nan"
i=0
for x in total_df["Team"]:
    try:
        total_df["Location"][i] = locations[x[4:]]
    except:
        total_df["Location"][i] = "None"
    i+=1


loc = []
for x in total_df["Location"]:
    if x == "None":
        x = "Blacksburg, Virginia"
    loc.append(x)

total_df["Location"] = loc






lats = {}
lons = {}
states = {}

key = OpenCageAPIKey
geocoder = OpenCageGeocode(key)
for location in total_df["Location"]:

    query = u''+ location +''
    results = geocoder.geocode(query)

    lat = results[0]['geometry']['lat']
    lon = results[0]['geometry']['lng']
    state = results[0]['components']['state']

    lats[location] = lat
    lons[location] = lon
    states[location] = state

total_df["lats"] = "Nan"
total_df["lons"] = "Nan"
total_df["state"] = "Nan"


i=0
test = []
for x in total_df["Location"]:
    if x in lats.keys():
        total_df["lats"][i] = lats[x]
        total_df["lons"][i] = lons[x]
        total_df["state"][i] = states[x]
    i+=1

state_dict = {}
i=0
for x in total_df["Team"]:
    name = x[4:]
    state_dict[name]=total_df["state"][i]
    i+=1

totals_df = total_df.loc[:, ['Team','Bball_win_pct', 'Bball_ortg', 'Bball_drtg','Bball_recruiting','Fball_win_pct', 'Fball_ortg', 'Fball_drtg', 'Fball_recruiting']].copy()

names = []
for x in totals_df["Team"]:
    names.append(x[4:])
totals_df["Team"] = names

totals_df["Bball_win_pct"] = pd.to_numeric(totals_df["Bball_win_pct"])
totals_df["Bball_ortg"] = pd.to_numeric(totals_df["Bball_ortg"])
totals_df["Bball_drtg"] = pd.to_numeric(totals_df["Bball_drtg"])
totals_df["Bball_recruiting"] = pd.to_numeric(totals_df["Bball_recruiting"])
totals_df["Fball_win_pct"] = pd.to_numeric(totals_df["Fball_win_pct"])
totals_df["Fball_ortg"] = pd.to_numeric(totals_df["Fball_ortg"])
totals_df["Fball_drtg"] = pd.to_numeric(totals_df["Fball_drtg"])
totals_df["Fball_recruiting"] = pd.to_numeric(totals_df["Fball_recruiting"])
totals_df = totals_df.groupby(totals_df["Team"]).mean()

schools = list(totals_df.index.values)

totals_df["Team"] = schools

df_2015 = total_df.copy()
df_2016 = total_df.copy()
df_2017 = total_df.copy()
df_2018 = total_df.copy()
df_2019 = total_df.copy()




pics_df = basketball_df.loc[:, ['Team','logos']].copy()

names = []
for x in pics_df["Team"]:
    names.append(x[4:])
pics_df["Team"] = names

please = []
for x in pics_df['logos']:
    please.append(x)

my_list = []
my_pics_list = []

i=0
for x in pics_df['Team']:
    if x not in my_list:
        my_list.append(x)
        my_pics_list.append(please[i])
    i+=1

pictures = pd.DataFrame(list(zip(my_list, my_pics_list)), columns =['Team', 'logo'])

df_2015 = df_2015[df_2015.Team.str.startswith("2015")]
df_2016 = df_2016[df_2016.Team.str.startswith("2016")]
df_2017 = df_2017[df_2017.Team.str.startswith("2017")]
df_2018 = df_2018[df_2018.Team.str.startswith("2018")]
df_2019 = df_2019[df_2019.Team.str.startswith("2019")]

year_list = [df_2015,df_2016,df_2017,df_2018,df_2019]
for years in year_list:
    names = []
    for x in years["Team"]:
        names.append(x[4:])
    years["Team"] = names




def add_better(df, length):
    wins = []
    off = []
    defe = []
    rec = []

    df["Win_pct"] = "nan"
    df["Offense"] = "nan"
    df["Defense"] = "nan"
    df["Recruiting"] = "nan"

    bball_win = list(df["Bball_win_pct"])
    fball_win = list(df["Fball_win_pct"])
    bball_o = list(df["Bball_ortg"])
    fball_o = list(df["Fball_ortg"])
    bball_d = list(df["Bball_drtg"])
    fball_d = list(df["Fball_drtg"])
    bball_r = list(df["Bball_recruiting"])
    fball_r = list(df["Fball_recruiting"])
    for x in range(length):
        if bball_win[x] > fball_win[x]:
            wins.append("Basketball")
        else:
            wins.append("Football")

        if bball_o[x] < fball_o[x]:
            off.append("Basketball")
        else:
            off.append("Football")

        if bball_d[x] < fball_d[x]:
            defe.append("Basketball")
        else:
            defe.append("Football")

        if bball_r[x] < fball_r[x]:
            rec.append("Basketball")
        else:
            rec.append("Football")

    df["Win_pct"] = wins
    df["Offense"] = off
    df["Defense"] = defe
    df["Recruiting"] = rec

add_better(df_2015, 118)
add_better(df_2016, 118)
add_better(df_2017, 119)
add_better(df_2018, 119)
add_better(df_2019, 119)
add_better(totals_df, 120)



all_df = total_df.copy()

all_df = all_df.set_index(all_df["Team"])

locations = total_df.loc[:, ['Team','lats', 'lons']].copy()
names = []
for x in locations["Team"]:
    names.append(x[4:])
locations["Team"] = names

locations = locations.groupby(locations["Team"]).sum()

schools_list = list(locations.index.values)

locations["lats"] = locations["lats"].div(5)
locations["lons"] = locations["lons"].div(5)

locations["Team"] = schools_list
locations["state"] = "nan"
i=0
for x in locations["Team"]:
    locations["state"][i] = state_dict[x]
    i+=1

locations["abbr"] = "nan"

states1 = {'al' : 'Alabama', 'ak' : 'Alaska', 'az' : 'Arizona', 'ar' : 'Arkansas', 'ca' : 'California', 'co' : 'Colorado', 'ct' : 'Connecticut', 'de' : 'Deleware', 'fl' : 'Florida', 'ga': 'Georgia', 'hi' : 'Hawaii', 'id' : 'Idaho', 'il' : 'Illinois', 'in' : 'Indiana', 'ia' : 'Iowa', 'ks' : 'Kansas', 'ky' : 'Kentucky', 'la' : 'Louisiana', 'me' : 'Maine', 'md' : 'Maryland', 'ma' : 'Massachusetts', 'mi' : 'Michigan', 'mn' : 'Minnesota', 'ms' : 'Mississippi', 'mo' : 'Missouri', 'mt' : 'Montana', 'ne' : 'Nebraska', 'nv' : 'Nevada', 'nh' : 'New Hampshire', 'nj' : 'New Jersey', 'nm' : 'New Mexico', 'ny' : 'New York', 'nc' : 'North Carolina', 'nd' : 'North Dakota', 'oh' : 'Ohio', 'ok' : 'Oklahoma', 'or' : 'Oregon', 'pa' : 'Pennsylvania', 'ri' : 'Rhode Island', 'sc' : 'South Carolina', 'sd' : 'South Dakota', 'tn' : 'Tennessee', 'ut' : 'Utah', 'vt' : 'Vermont', 'va' : 'Virginia', 'wa' : 'Washington', 'wv' : 'West Virginia', 'wi' : 'Wisconsin', 'wy' :'Wyoming', 'tx' : 'Texas'}
x2 = list(states1.keys())
y2 = list(states1.values())





states_dict = {}
i = 0
y = []
r=list(states1.values())
for x in x2:
    up = x.upper()
    y.append(up)
for state in y2:
    states_dict[state] = y[i]
    i+=1

i=0
for x in locations["state"]:
    locations["abbr"][i]=states_dict[x]
    i+=1


df_2015 = df_2015.fillna(200)
df_2017 = df_2017.fillna(200)
df_2016 = df_2016.fillna(200)




DBNAME = "college_sports.db"

def create_location_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'locations';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "locations" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "latitude"    INTEGER,
    "longitude"    INTEGER,
    "State"    TEXT,
    "abbr"    TEXT);
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()




def create_2015_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'fifteen';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "fifteen" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "Conference"    TEXT,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Location"    TEXT,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,

    FOREIGN Key(School) REFERENCES locations(School));

    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def create_2016_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'sixteen';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "sixteen" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "Conference"    TEXT,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Location"    TEXT,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,


    FOREIGN Key(School) REFERENCES locations(School));
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


def create_2017_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'seventeen';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "seventeen" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "Conference"    TEXT,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Location"    TEXT,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,

    FOREIGN Key(School) REFERENCES locations(School));
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()



def create_2018_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'eighteen';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "eighteen" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "Conference"    TEXT,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Location"    TEXT,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,

    FOREIGN Key(School) REFERENCES locations(School));
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()



def create_2019_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'nineteen';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "nineteen" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "Conference"    TEXT,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Location"    TEXT,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,

    FOREIGN Key(School) REFERENCES locations(School));


    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


def create_pics_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'pics';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "pics" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "logo"    TEXT,

    FOREIGN Key(School) REFERENCES locations(School));

    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


def create_totals_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'totals';"
    cur.execute(statement)

    statement = '''
    CREATE TABLE "totals" (
    "School"    TEXT PRIMARY KEY UNIQUE,
    "bball_win_pct"    INTEGER,
    "bball_ortg"    INTEGER,
    "bball_drtg"    INTEGER,
    "bball_recruiting"    INTEGER,
    "fball_win_pct"    INTEGER,
    "fball_ortg"    INTEGER,
    "fball_drtg"    INTEGER,
    "fball_recruiting"    INTEGER,
    "Wins_pct"    INTEGER,
    "Offense"    INTEGER,
    "Defense"    INTEGER,
    "Recruiting"    INTEGER,

    FOREIGN Key(School) REFERENCES locations(School));
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

create_location_table()
create_2015_table()
create_2016_table()
create_2017_table()
create_2018_table()
create_2019_table()
create_pics_table()
create_totals_table()



DBNAME = "college_sports.db"
def insert_years_2015(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Conf"].tolist(),df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Location"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i], list1[13][i], list1[14][i])
        i+=1
        statement = 'INSERT INTO "fifteen"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_years_2016(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Conf"].tolist(),df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Location"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i], list1[13][i], list1[14][i])
        i+=1
        statement = 'INSERT INTO "sixteen"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_years_2017(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Conf"].tolist(),df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Location"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i], list1[13][i], list1[14][i])
        i+=1
        statement = 'INSERT INTO "seventeen"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_years_2018(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Conf"].tolist(),df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Location"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i], list1[13][i], list1[14][i])
        i+=1
        statement = 'INSERT INTO "eighteen"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_years_2019(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Conf"].tolist(),df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Location"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i], list1[13][i], list1[14][i])
        i+=1
        statement = 'INSERT INTO "nineteen"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_totals(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(), df_name["Bball_win_pct"].tolist(),df_name["Bball_ortg"].tolist(),df_name["Bball_drtg"].tolist(),df_name["Bball_recruiting"].tolist(),df_name["Fball_win_pct"].tolist(),df_name["Fball_ortg"].tolist(),df_name["Fball_drtg"].tolist(),df_name["Fball_recruiting"].tolist(),df_name["Win_pct"].tolist(),df_name["Offense"].tolist(),df_name["Defense"].tolist(),df_name["Recruiting"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i], list1[5][i], list1[6][i], list1[7][i], list1[8][i], list1[9][i], list1[10][i], list1[11][i], list1[12][i])
        i+=1
        statement = 'INSERT INTO "totals"'
        statement +='VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_locations(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [schools_list, df_name["lats"].tolist(),df_name["lons"].tolist(),df_name["state"].tolist(),df_name["abbr"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i], list1[2][i], list1[3][i], list1[4][i])
        i+=1
        statement = 'INSERT INTO "locations"'
        statement +='VALUES (?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def insert_pics(df_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    list1 = []
    list1 = [df_name["Team"].tolist(),df_name["logo"].tolist()]

    i = 0
    for x in list1[0]:
        insertion = (x, list1[1][i])
        i+=1
        statement = 'INSERT INTO "pics"'
        statement +='VALUES (?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()


insert_years_2015(df_2015)
insert_years_2016(df_2016)
insert_years_2017(df_2017)
insert_years_2018(df_2018)
insert_years_2019(df_2019)
insert_totals(totals_df)
insert_locations(locations)
insert_pics(pictures)
