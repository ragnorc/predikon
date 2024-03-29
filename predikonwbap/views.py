from datetime import datetime as dt
from datetime import time
from flask import render_template, g, jsonify
from predikondata import Vote, Prediction, Result
from predikonwbap import app
import sqlite3

# State variables.
NOW = dt.now
# NOW = lambda: dt(2019, 2, 10, 12, 10)
PREDICT_AT = None
# PREDICT_AT = dt(2019, 2, 10, 12, 3, 13)
# PREDICT_AT = dt(2019, 2, 10, 12, 59, 33)
# PREDICT_AT = dt(2019, 2, 10, 16, 28, 57)


def num_non_empty(results):
    return len([r for r in results if r.yes_percent is not None])


def format_number(num, percent=False):
    if num is not None:
        if percent:
            return float(f'{num*100:.2f}')
        else:
            return float(f'{num:.2f}')
    else:
        return 0


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('predikon.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

with app.app_context():
    res = query_db('SELECT id, title_fr from vote')
    voteList = [{'id': id, 'title' : title} for id,title in res]
    res = query_db('SELECT ogd_id, population_size, area, name, flag, postal_code, canton, language, svd_1, svd_2, tsne_1, tsne_2 FROM municipality')
    mcpDict = {id : {"pop": pop, "area": area, "name": name, "flag": flag, "postal_code": postal_code, "canton": canton, "language":language,"svd_1":svd_1,"svd_2":svd_2, "tsne_1":tsne_1,"tsne_2":tsne_2 } for id,pop,area,name,flag,postal_code,canton,language,svd_1,svd_2,tsne_1,tsne_2 in res}
    


@app.route('/')
def index():
    votes_query = (Vote
                   .select()
                   .where(Vote.vote_day.year >= NOW().year)
                   .order_by(Vote.vote_day.desc()))
    votes = list()
    for vote in votes_query.namedtuples():
        # Check if vote is live.
        is_live = (NOW().date() == vote.vote_day) and (NOW().time() > time(12))
        # DEBUG {
        if PREDICT_AT is not None:
            pred = Prediction.select().where(
                Prediction.timestamp == PREDICT_AT).get()
            res = Result.get_at(PREDICT_AT, vote.id, non_empty=False)
        # }
        else:
            # Get prediction.
            pred = Prediction.get_or_none(Prediction.vote_id == vote.id)
            res = Result.get_latest(vote.id, non_empty=False)
            # Get current count.
            yes_count = sum([r.num_yes for r in res if r.num_yes is not None])
            valid = sum([r.num_valid for r in res if r.num_valid is not None])
            if valid > 0:
                count = yes_count / valid
            else:
                count = 0
        # Get progress of counting.
        if len(res) > 0:
            # counting = num_non_empty(res) / len(res)
            total_eligible = 5305654
            counting = sum([r.num_eligible for r in res
                     if r.num_eligible is not None])
            counting = counting / total_eligible
        else:
            counting = 0
        # Check prediction.
        if pred is not None:
            yp = pred.yes_predicted
        else:
            yp = 0
        # Construct vote object for front end.
        votes.append({
            'id': vote.id,
            'title': vote.title_fr,
            'yes_percent':  format_number(vote.yes_percent, percent=True),
            'turnout': format_number(vote.turnout, percent=True),
            'count': format_number(count, percent=True),
            'prediction': format_number(yp, percent=True),
            'vote_day': vote.vote_day,
            'is_final': vote.is_final,
            'is_live': is_live,
            'counting': int(counting * 100)
        })
        

    return render_template('index.html', votes=votes, voteList=voteList)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/patterns')
def patterns():
    return render_template('patterns.html', voteList=voteList, mcpDict=mcpDict)

@app.route('/remapping')
def remapping():
    return render_template('remapping.html', voteList=voteList, mcpDict=mcpDict)


@app.route('/vote_results/<int:id>')
def vote_results(id):
    res = query_db('SELECT municipality.ogd_id, result.num_yes, result.num_total, municipality.population_size, municipality.area, municipality.name, municipality.flag, municipality.postal_code, municipality.language, vote.title_fr FROM result, municipality, vote where result.municipality_id == municipality.id AND vote.id == result.vote_id AND vote.id =={}'.format(id))
    voteDict = {id : { "numYes": numYes, "numTotal" : numTotal, "pop": pop, "area": area, "name": name, "flag": flag, "postal_code": postal_code, "language":language, "title":title} for id,numYes,numTotal,pop,area,name,flag,postal_code,language,title in res}
    print(voteDict.popitem())
    return render_template('vote_results.html', voteList=voteList, voteDict=voteDict, title=voteDict.popitem()[1]["title"])

