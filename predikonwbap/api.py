from flask import jsonify, send_from_directory
from predikondata import Result
from predikonwbap import app
import sqlite3
import os
from flask import g


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

@app.route('/get_data')
def get_data():
    res = Result.get()
    return jsonify({'data': res.id})


@app.route('/get_votes')
def get_votes():
    res = query_db('SELECT municipality.ogd_id, result.num_yes, result.num_total FROM result, municipality, vote where result.municipality_id == municipality.id AND vote.id == result.vote_id AND vote.id == 2')
    dicti = dict((a,[b,c]) for a,b,c in res)
    return jsonify({'data': dicti})