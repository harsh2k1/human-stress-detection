from .api.monitor_api import monitor_api_router
from .api.prediction_api import prediction_api_router
from .api.login_api import login_api_router
from .services.config_service import read_config, StoreToConfigAction
from .utils import api_models
from .services.identifier_generation import generate_hash_uid

config = read_config()