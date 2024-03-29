from flask import jsonify, send_from_directory
from predikondata import Result
from predikonwbap import app
from flask import g
import sqlite3
import os



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


@app.route('/get_vote_results/<int:id>')
def get_vote_results(id):
    res = query_db('SELECT municipality.ogd_id, result.num_yes, result.num_total, municipality.population_size, municipality.area, municipality.name, municipality.flag, municipality.postal_code, municipality.language FROM result, municipality, vote where result.municipality_id == municipality.id AND vote.id == result.vote_id AND vote.id =={}'.format(id))
    voteDict = {id : { "numYes": numYes, "numTotal" : numTotal, "pop": pop, "area": area, "name": name, "flag": flag, "postal_code": postal_code, "language":language} for id,numYes,numTotal,pop,area,name,flag,postal_code,language in res}
    return jsonify({'data': voteDict})


@app.route('/get_mcp_data')
def get_mpc_data():
    res = query_db('SELECT name, ogd_id, postal_code  FROM municipality')
    mcpDict = {ogd_id: {"title": name, "ogd_id":ogd_id, "postal_code": postal_code, "category": "Municipality"} for name, ogd_id, postal_code in res}
    return jsonify({'data': mcpDict})


@app.route('/get_vote_data')
def get_vote_data():
    res = query_db('SELECT title_fr, ogd_id, id  FROM vote')
    voteDict = {ogd_id: {"title": title, "ogd_id":ogd_id, "vote_id":vote_id, "category": "Vote"} for title, ogd_id, vote_id in res}
    return jsonify({'data': voteDict})