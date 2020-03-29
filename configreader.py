import configparser as cp

"""
Read the external configurations
Input parameter: 
    filename
Returns cnfig Object
"""
def config_reader(filename):
    try:
        config = cp.RawConfigParser()
        config.read(filename)
    except Exception as error:
        logger.error('Error reading configuration file {}' .format(error))

    return config