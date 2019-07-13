from flask import Flask, render_template, url_for, flash, redirect, jsonify, session, request
from forms import SearchForm
import database_query
import matching_freeform
app = Flask(__name__) #create app variable, set to instance of fla sk class, __name__ = name of module

app.config['SECRET_KEY'] = 'e311111111111111111111111111111b'

@app.route("/", methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        object = form.search.data
        session['searchterm'] = object
        return redirect(url_for('match'))
    return render_template('search.html', title = 'Search', form=form)

@app.route("/match", methods = ['GET', 'POST'])
def match():
    searchterm = session.get('searchterm', None)
    choices = matching_freeform.top5(searchterm)
    return render_template('match.html', choices = choices)

@app.route("/query", methods = ['GET', 'POST'])
def query():
    selected_choice = request.args.get('type') #https://stackoverflow.com/questions/50426137/flask-get-clicked-link-info-and-display-on-rendered-page
    data = matching_freeform.get_rows(selected_choice)

    name = data.iloc[0,2]
    type = data.iloc[0,9]
    length = data.iloc[0,10]
    definition = data.iloc[0, 4]
    tables = data['TABNAME']

    unique = tables.unique().tolist()

    return render_template('query.html', title = name, definition = definition, tables = unique,
                           type = type, length = length)

if __name__ == '__main__':
    app.run(debug=True)
