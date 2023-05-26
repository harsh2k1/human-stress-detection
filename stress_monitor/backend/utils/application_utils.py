from argparse import ArgumentParser
from backend import StoreToConfigAction

parser = ArgumentParser()
parser.add_argument("-port", "--port", help="Port to host the backend application", default=8000, type=int, action=StoreToConfigAction)
vars(parser.parse_args())