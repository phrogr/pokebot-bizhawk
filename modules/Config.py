import os
import logging
import fastjsonschema
from ruamel.yaml import YAML

log = logging.getLogger(__name__)

yaml = YAML()
yaml.default_flow_style = False

config_schema = {
    "type": "object",
    "properties": {
        "bot_mode": {"type": "string"},
        "coords": {"type": "object",
                   "properties": {
                       "pos1": {"type": "array"},
                       "pos2": {"type": "array"}
                   }
                   },
        "direction": {"type": "string"},
        "starter": {"type": "string"},
        "johto_starter": {"type": "string"},
        "fossil": {"type": "string"},
        "deoxys_puzzle_solved": {"type": "boolean"},
        "ui": {"type": "object",
               "properties": {
                   "enable": {"type": "boolean"},
                   "width": {"type": "number"},
                   "height": {"type": "number"}
               }
               },
        "server": {"type": "object",
                   "properties": {
                       "enable": {"type": "boolean"},
                       "ip": {"type": "string"},
                       "port": {"type": "number"}
                   }
                   },
        "discord": {"type": "object",
                    "properties": {
                        "enable": {"type": "boolean"},
                        "webhook_url": {"type": "string"},
                        "iv_format": {"type": "string"}
                    }
                    },
        "periodic_save": {"type": "boolean"},
        "save_every_x_encounters": {"type": "number"},
        "manual_catch": {"type": "boolean"},
        "use_spore": {"type": "boolean"},
        "catch_shinies": {"type": "boolean"},
        "battle_others": {"type": "boolean"},
        "pokeball_override": {"type": "object"},
        "cycle_lead_pokemon": {"type": "boolean"},
        "save_game_after_catch": {"type": "boolean"},
        "pickup": {"type": "boolean"},
        "pickup_threshold": {"type": "number"},
        "log": {"type": "boolean"},
        "bot_instance_id": {"type": "string"},
        "banned_moves": {"type": "array"},
        "mem_hacks": {"type": "boolean"}
    }
}

ConfigValidator = fastjsonschema.compile(config_schema)  # Validate the config file to ensure user didn't do a dumb


def GetConfig():
    file = "config.yml"
    if os.path.exists(file):
        with open(file, mode="r", encoding="utf-8") as f:
            config = yaml.load(f)
            try:
                ConfigValidator(config)
                config["bot_mode"] = config["bot_mode"].lower()
                log.info("Config is valid!")
                return config
            except fastjsonschema.exceptions.JsonSchemaDefinitionException as e:
                log.error(str(e))
                log.error("Config is invalid!")
                return None
    else:
        log.error("Config file not found!")
        return None
