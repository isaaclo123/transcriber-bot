"""Configuration values for the reddit transcriber bot"""

import os
import json
import configparser

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "config.ini"

class Config(object):
    """a wrapper class for the ConfigParser config"""
    def __init__(self, file_path):
        """constructor for config class

        :file_path: file path where config file should be

        """

        config = Config.read_config(file_path)

        # if config file does not have proper parts yet, create it
        if not config["DEFAULT"]:
            config = Config.create_config(file_path)

        # debug var
        self.debug = config["DEFAULT"]["debug"].lower() == "true"

        self.client_id = config["DEFAULT"]["client_id"]
        self.client_secret = config["DEFAULT"]["client_secret"]
        self.user_agent = config["DEFAULT"]["user_agent"]
        self.username = config["DEFAULT"]["username"]
        self.password = config["DEFAULT"]["password"]
        self.subreddits = json.loads(config["DEFAULT"]["subreddits"])


    @staticmethod
    def create_config(file_path):
        """Creates a ConfigParser config object for the transcriber bot

        :file_path: file path to place config file
        :returns: ConfigParser config object

        """

        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "debug": "True",
            "client_id": "$CLIENT ID GOES HERE$",
            "client_secret": "$SECRET GOES HERE$",
            "user_agent": "transcriber_bot 1 (by /u/isaac_lo)",
            "username": "$REDDIT USERNAME GOES HERE$",
            "password": "$REDDIT PASSWORD GOES HERE$",
            "subreddits": "[\"testingground4bots\"]"
        }

        config_file_path = os.path.join(file_path, CONFIG_FILE)

        # write to config file
        with open(config_file_path, "w") as config_file:
            config.write(config_file)

        print("Config file {} created".format(config_file_path))

        return config

    @staticmethod
    def read_config(file_path):
        """Reads a ConfigParser config and returns the object

        :file_path: file path of config file
        :returns: ConfigParser config object

        """
        config = configparser.ConfigParser()
        config_file_path = os.path.join(file_path, CONFIG_FILE)
        config.read(config_file_path)

        print("Config file {} opened".format(config_file_path))
        return config
