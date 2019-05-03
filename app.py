import os

from flask import Flask, Response
from flask import render_template, redirect


app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('index.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


if __name__ == '__main__':
    app.run(debug=True)