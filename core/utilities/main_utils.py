from argparse import ArgumentParser
import sys
sys.path.append("")
from core.service.config_service import set_custom_config

parser = ArgumentParser()

parser.add_argument('-p', '--PORT', help="PORT", required=True)

args = vars(parser.parse_args())

set_custom_config({"APPLICATION":args})


