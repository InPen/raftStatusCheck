# app/routes.py
from flask import Blueprint, render_template
from app.models import Case

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    cases = Case.query.all()
    return render_template("index.html", cases=cases)
