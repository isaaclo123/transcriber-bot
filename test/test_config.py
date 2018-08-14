"""Configuration values for the reddit transcriber bot"""

import os
from transcriber_bot.config import Config

CONFIG_FILE = "config.ini"

def test_config_constructor_firstrun(tmpdir):
    """test that the firstrun flag is true when no prior config"""
    config = Config(tmpdir)
    assert config.firstrun

def test_config_constructor_valid(tmpdir):
    """test that the config reads properly after created"""
    # create default config file
    Config(tmpdir)
    # read config file
    config = Config(tmpdir)
    # assert not first config run
    assert not config.firstrun

    config_default = {
        "debug": "True",
        "client_id": "$CLIENT ID GOES HERE$",
        "client_secret": "$SECRET GOES HERE$",
        "user_agent": "transcriber_bot 1 (by /u/isaac_lo)",
        "username": "$REDDIT USERNAME GOES HERE$",
        "password": "$REDDIT PASSWORD GOES HERE$",
        "subreddits": "[\"testingground4bots\"]"
    }

    assert config.debug
    assert config.client_id == config_default["client_id"]
    assert config.client_secret == config_default["client_secret"]
    assert config.user_agent == config_default["user_agent"]
    assert config.username == config_default["username"]
    assert config.password == config_default["password"]
    assert config.subreddits == ["testingground4bots"]

def test_config_read_config(tmpdir):
    """test that the read_config reads properly"""
    # create config.
    config1 = Config.create_config(tmpdir)["DEFAULT"]
    config2 = Config.read_config(tmpdir)["DEFAULT"]

    assert config1["debug"] == config2["debug"]
    assert config1["client_id"] == config2["client_id"]
    assert config1["client_secret"] == config2["client_secret"]
    assert config1["user_agent"] == config2["user_agent"]
    assert config1["username"] == config2["username"]
    assert config1["password"] == config2["password"]
    assert config1["subreddits"] == config2["subreddits"]

def test_create_config(tmpdir):
    """test that create_config works"""
    # create a config
    config = Config.create_config(tmpdir)["DEFAULT"]

    # check if config.ini is a file in tmpdir
    assert os.path.isfile(os.path.join(tmpdir, CONFIG_FILE))

    config_default = {
        "debug": "True",
        "client_id": "$CLIENT ID GOES HERE$",
        "client_secret": "$SECRET GOES HERE$",
        "user_agent": "transcriber_bot 1 (by /u/isaac_lo)",
        "username": "$REDDIT USERNAME GOES HERE$",
        "password": "$REDDIT PASSWORD GOES HERE$",
        "subreddits": "[\"testingground4bots\"]"
    }

    # assert that a proper default config has been created
    assert config["debug"] == config_default["debug"]
    assert config["client_id"] == config_default["client_id"]
    assert config["client_secret"] == config_default["client_secret"]
    assert config["user_agent"] == config_default["user_agent"]
    assert config["username"] == config_default["username"]
    assert config["password"] == config_default["password"]
    assert config["subreddits"] == config_default["subreddits"]
