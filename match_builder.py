from pymongo import MongoClient
import json
from os import path
from config import *


def build_match(tournament_id, match_id):
    db = _setup_db()
    match, teams = _get_data_from_tournament(db, tournament_id, match_id)
    _add_steamids_to_teams(db, teams)
    damn = _find_players_with_schizophrenia(teams)
    if len(damn):
        print('Player {} can only be on one team!'.format(', '.join(damn)))
    return _build_and_dump_json(match, teams)


def _setup_db():
    client = MongoClient('mongodb://127.0.0.1:3001')
    return client.meteor


def _get_data_from_tournament(db, tournament_id, match_id):
    tournament = db.tournaments.find_one({'_id': tournament_id})
    match, = (m['match'] for m in tournament['challongeData']['tournament']['matches'] if str(m['match']['id']) == match_id)
    if not match:
        raise Exception('SHIT')
    participants = [
        p['participant']['misc']
            for p in tournament['challongeData']['tournament']['participants']
                if p['participant']['id']
                    in [match['player1_id'], match['player2_id']]]

    teams = []
    for p in participants:
        teams.append(db.teams.find_one({'_id': str(p)}))
    return (match, teams)


def _add_steamids_to_teams(db, teams):
    for i, team in enumerate(teams):
        teams[i]['steam_ids'] = [user['profile']['id'] for user in db.users.find({'_id': {'$in': team['playerUserIds']}}, {'profile.id': 1, '_id': 0})]
    return teams


def _find_players_with_schizophrenia(teams):
    return set(teams[0]['steam_ids']) & set(teams[1]['steam_ids'])


def _build_and_dump_json(match, teams, map_list=std_map_pool):
    match_json = {
        'matchid': str(match['id']),
        'match_title': 'Round ' + str(match['round']) + ' | Map {MAPNUMBER} of {MAXMAPS}',
        'maps_to_win': 2,
        'side_type': 'standard',
        'maplist': map_list,
    }

    for i, team in enumerate(teams):
        match_json['team' + str(i + 1)] = {
            'name': team['name'],
            'players': team['steam_ids']
        }

    abs_path = ''
    with open(str(match['id']) + '.json', 'w') as f:
        json.dump(match_json, f, indent=4, sort_keys=True)
        abs_path = path.abspath(f.name)
    return abs_path
