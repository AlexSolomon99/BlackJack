import os

import logger
import blackjack_game
import utils

# set up the logger
log_conf_path = r"./conf/log_conf.txt"
log = logger.BJLog(conf_file_path=log_conf_path).create_logger(app_name="BlackJack")
log.info(f"Start game!")

# config path
log.info(f"Get the game configuration")
base_conf = r"./conf"
game_config_path = os.path.join(base_conf, "game_config.json")
game_config = utils.read_json(game_config_path)

app = blackjack_game.BlackJack(game_config=game_config,
                               deterministic=True,
                               log=log)

log.info(f"App finished!")


