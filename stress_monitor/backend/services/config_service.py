import configparser
import sys
import argparse
sys.path.append("")
sys.dont_write_bytecode = True

class StoreToConfigAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Store the value to the configuration file
        config = configparser.ConfigParser()
        config.read('backend/config/runtime.cfg')
        config['APPLICATION']['port'] = str(values)
        
        with open('backend/config/runtime.cfg', 'w') as configfile:
            config.write(configfile)
        
        import backend
        backend.config = read_config()


def set_default_path(project_path):
    config = read_config()

    # Save the project path in the config file
    config["PATH"] = {"project_path": project_path}
    with open("config/application.cfg", "w") as configfile:
        config.write(configfile)


def set_custom_config(**kwargs):
    config = read_config()
    config.update(kwargs)
    with open("config/global_config.cfg", "w") as configfile:
        config.write(configfile)


def read_config():
    """
    The function to give config according to selected enviornment

    Parameters:
        No parameters

    Returns:
        config parser object with selected configuration
    """

    config_parser = configparser.ConfigParser()

    import os
    import glob
    for file in glob.glob(os.path.join("backend/config", "*.cfg")):
        config_parser.read(file)
    
    return config_parser
