import configparser
import sys
sys.path.append("")
sys.dont_write_bytecode = True


def set_default_path(project_path):
    config = read_config()

    # Save the project path in the config file
    config["PATH"] = {"project_path": project_path}
    with open("config/application.cfg", "w") as configfile:
        config.write(configfile)


def set_custom_config(args):
    config = read_config()
    config.update(args)
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
    config_parser.read("config/application.cfg")
    config_parser.read("config/global_config.cfg")

    return config_parser
