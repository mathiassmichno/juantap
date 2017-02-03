import falcon
import os

class CsgoServer(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = (os.urandom(1000))

app = falcon.API()

csgo_server = CsgoServer()

app.add_route('/server', csgo_server)

# from match_builder import build_match
# import begin
#
# @begin.start(short_args=True)
# def main(match_id: 'Challonge Match ID', tournament_id: 'Mongo Tournament ID'):
#     """ CSGO server tools 4 CSGO Hub """
#     filename = build_match(tournament_id=tournament_id, match_id=match_id)
#     print(filename)
#
# # 'X56hRniQBES5dCaQA'
# # '67948184'
