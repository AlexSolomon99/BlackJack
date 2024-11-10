import os

import logger
import blackjack_game
import utils

# set up the logger
log_conf_path = r"./conf/log_conf.txt"
logs_path = r"./logs"
if not os.path.isdir(logs_path):
    os.mkdir(logs_path)

log = logger.BJLog(conf_file_path=log_conf_path).create_logger(app_name="BlackJack")
log.info(f"Start game!")

# config path
log.info(f"Get the game configuration")
base_conf = r"./conf"
game_config_path = os.path.join(base_conf, "game_config.json")
game_config = utils.read_json(game_config_path)

# the game resets when initiated
app = blackjack_game.BlackJack(game_config=game_config,
                               deterministic=True,
                               log=log)

log.info(f"Player dictionary: {app.players_dict}")
log.info(f"Game deck: {app.deck}")

# play one game
app.play_one_game()

log.info(f"App finished!")


