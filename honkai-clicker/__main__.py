import logging
import sys
import traceback
from HonkaiClicker import HonkaiClicker, Challenge, ChallengeType, ResourceType


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    clicker = HonkaiClicker()
    challenges = [
        Challenge(ChallengeType.SEPAL_GOLD, ResourceType.MONEY, 24),
        #Challenge(ChallengeType.SEPAL_GOLD, ResourceType.CHARACTER_EXP, 24),
        #Challenge(ChallengeType.SEPAL_GOLD, ResourceType.WEAPON_EXP, 1)
    ]

    try:
        clicker.start_game("S:\Games\Star Rail\Games\StarRail.exe")
        clicker.login()
        clicker.accomplish_challenges(challenges)
    except:
        logging.error(traceback.format_exc())

    clicker.kill_game()
