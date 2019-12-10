import model
import sqlite3
from flask import Flask, render_template, g, request
app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect(model.DATABASE)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    schools = ['latitude', 'longitude', 'state']
    if request.method == "POST":
        z = request.form["schools"]
        please = model.get_locations(z)
    else:
        please = model.get_locations()
    return render_template("index.html", schools=schools, please=please)

@app.route('/school', methods=['GET', 'POST'])
def school_page():
    years = model.years
    comparisons = model.comparisons
    schools = model.schools_list
    school_selected = 'Air Force'
    year_selected = '2015'
    comparison_selected = 'Wins_pct'
    if request.method == "POST":
        school_selected = request.form["schools"]
        year_selected = request.form["year"]
        comparison_selected = request.form["compare"]
        result = model.search_by_school(school_selected,year_selected,comparison_selected)
        url = model.get_pic(school_selected)
    else:
        result = model.search_by_school()
        url = model.get_pic()
    return render_template("school.html", schools=schools, comparisons=comparisons, years=years, result=result, x = school_selected, y = year_selected, z = comparison_selected, url=url)

@app.route('/state', methods=['GET', 'POST'])
def state_page():
    states = model.states
    comparisons = model.comparisons
    years = model.years
    state_selected = 'Hawaii'
    year_selected = '2015'
    comparison_selected = 'Wins_pct'
    if request.method == "POST":
        state_selected = request.form["state"]
        year_selected = request.form["year"]
        comparison_selected = request.form["compare"]
        result = model.search_by_state1(state_selected, year_selected, comparison_selected)
        result2 = model.search_by_state2(state_selected, year_selected, comparison_selected)
        result3 = model.search_by_state3(state_selected, year_selected, comparison_selected)
        graph = model.graph_states(year_selected, comparison_selected, state_selected)
    else:
        result = model.search_by_state1()
        result2 = model.search_by_state2()
        result3 = model.search_by_state3()
        graph = model.graph_states()
    return render_template("state.html", states=states, comparisons=comparisons, years=years, result=result, result2=result2, x = state_selected, y = year_selected, z = comparison_selected, result3=result3, graph=graph)



@app.route('/overview', methods=['GET', 'POST'])
def overview_page():
    comparisons = model.comparisons
    years = model.years
    year_selected = "2015"
    comparison_selected = "Wins_pct"
    if request.method == "POST":
        year_selected = request.form["year"]
        comparison_selected = request.form["compare"]
        result = model.overview_search(year_selected,comparison_selected)
        result1 = model.overview_search1(year_selected,comparison_selected)
        basketball = model.graph_basketball(year_selected, comparison_selected)
        # football = model.graph_football(year_selected, comparison_selected)
        # bar = model.create_plot()
    else:
        result = model.overview_search()
        result1 = model.overview_search1()
        basketball = model.graph_basketball()
        # football = model.graph_football()

        # bar = model.test_graph()
        # bar = model.create_plot()

    return render_template("overview.html", comparisons=comparisons, years=years, result=result, result1=result1, y=year_selected, z=comparison_selected, basketball=basketball)




if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)

















    # end
