from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Team, team_schema, teams_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/teams', methods = ['POST'])
@token_required
def add_team(current_user_token):
    name = request.json['name']
    team_name = request.json['team_name']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    add_team = Team(name, team_name, user_token = user_token )

    db.session.add(add_team)
    db.session.commit()

    response = team_schema.dump(add_team)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['GET'])
@token_required
def get_single_team(current_user_token, id):
    team = Team.query.get(id)
    response = team_schema.dump(team)
    return jsonify(response)

@api.route('/teams', methods = ['GET'])
@token_required
def get_teams(current_user_token):
    a_user = current_user_token.token
    teams = Team.query.filter_by(user_token = a_user).all()
    response = teams_schema.dump(teams)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['POST','PUT'])
@token_required
def update_team(current_user_token,id):
    team = Team.query.get(id) 
    team.name = request.json['name']
    team.team_name = request.json['team_name']
    team.user_token = current_user_token.token

    db.session.commit()
    response = team_schema.dump(team)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['DELETE'])
@token_required
def delete_team(current_user_token, id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()
    response = team_schema.dump(team)
    return jsonify(response)