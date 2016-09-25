from match_builder import build_match
import argparse

def main():
    print('sup')
    args = parse_args()
    print(args)
    filename = build_match(tournament_id=args.tournamentid, match_id=args.matchid)
    print(filename)


def parse_args():
    parser = argparse.ArgumentParser(description='CSGO server tools 4 CSGO Hub')
    parser.add_argument('-m', '--matchid',
                    help='Challonge match id', required=True)
    parser.add_argument('-t', '--tournamentid',
                    help='Mongo tournament id', required=True)

    return parser.parse_args()

if __name__ == '__main__':
    main()

# 'X56hRniQBES5dCaQA'
# '67948184'
