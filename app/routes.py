# app/routes.py
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "<h1>RAFT Status Tracker it works! Woohoo🎉</h1>"
    # later we'll use: return render_template("index.html")
