from flask import Flask, Blueprint, render_template, url_for, request, jsonify, current_app
import requests
import json

# Create a blueprint
bp = Blueprint('bp', __name__)

# from now on, url_for(.) in static HTML files should go for e.g. 'bp.opclick' instead of simply 'opclick'
@bp.route("/")
def index():
    return render_template("calc.html", outRes="", outExpr="", outState="calculate something!")

@bp.route("/opclick", methods=["POST"])
def opclick():
    data = request.get_json()
    print(f"client sent: num={data['number']} , sym={data['symbol']}")
    current_app.calc.add_symbol(data['symbol'] , data['number'])
    current_app.calc.print_state()
    return jsonify( current_app.calc.state )

@bp.route("/clear", methods=["POST"])
def clear():
    current_app.calc.reset()
    print(f"calculator reset") 
    return jsonify( current_app.calc.state )

