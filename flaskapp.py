from flask import Flask,render_template
from scraper import Page
import pandas as pd
app = Flask(__name__)


test = Page()


@app.route('/')
def hello_world():
    return render_template("ThePage.html",json_plotly_graph=test.pie_chart(),test=test.users_positon_table())
app.run(debug=True)