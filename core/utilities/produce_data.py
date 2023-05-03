import sys
sys.path.append("")
from core.service.kafka_service import Producer, Consumer

from argparse import ArgumentParser

parser = ArgumentParser()

# parser.add_argument('-m', '--mode', help='Mode: csv/vision', default='csv')
subparsers = parser.add_subparsers(dest='mode', help="Choose a mode: csv/vision", required=True)
csv_parser = subparsers.add_parser('csv', help='Mode=csv')
csv_parser.add_argument('-f','--file', help="Path of csv", required=True)

vision_parser = subparsers.add_parser('vision', help='Mode=vision')
vision_parser.add_argument('-f','--file', help="Path of vision py file", required=True)

args = vars(parser.parse_args())

def produce_from_csv(filepath, key=b'user1'):
    import pandas as pd

    df = pd.read_csv(filepath)
    data = df.iloc[:,0].to_list()
    count=0
    for val in data:
        if val>50:
            Producer().send_msg(key=key, msg=val)
            count += 1
    print(f"Dumped {count} values")
    

if __name__ == "__main__":
    if args['mode'] == 'csv':
        produce_from_csv(filepath=args['file'])
