import configparser


def config():
    """
    The function to give config according to selected enviornment

    Parameters:
        No parameters

    Returns:
        config parser object with selected configuration
    """

    config_parser = configparser.ConfigParser()
    config_parser.read("/Users/harshpreetsingh/Documents/minor-project/final_pipeline/config/application.cfg")

    return config_parser
