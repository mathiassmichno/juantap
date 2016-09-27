from match_builder import build_match
import begin

@begin.start(short_args=True)
def main(match_id: 'Challonge Match ID' = None, tournament_id: 'Mongo Tournament ID' = None):
    """ CSGO server tools 4 CSGO Hub """
    filename = build_match(tournament_id=tournament_id, match_id=match_id)
    print(filename)

if __name__ == '__main__':
    main()

# 'X56hRniQBES5dCaQA'
# '67948184'
