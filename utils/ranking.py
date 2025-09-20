import pandas as pd
from flask import Blueprint, render_template

ranking_bp = Blueprint('ranking', __name__)

def calculate_driver_rankings(results_csv="dataset/driver_ranking.csv"):
    df = pd.read_csv(results_csv)
    df = df.groupby(['year', 'surname'])['points'].sum().reset_index()
    latest_year = df['year'].max()
    df = df[df['year'] == latest_year]
    df = df.sort_values('points', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
    return df[['rank', 'surname', 'points']]

@ranking_bp.route("/ranking")
def ranking():
    df = calculate_driver_rankings()
    return render_template("ranking.html", tables=[df.to_html(classes='data', index=False)])
