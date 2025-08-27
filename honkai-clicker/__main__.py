from HonkaiClicker import HonkaiClicker
from PlanPerformer import Plan, PlanPerformer
from Types import *
import logging
import sys
import traceback


GAME_EXECUTABLE = r"S:\Games\Star Rail Games\StarRail.exe"


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    clicker = HonkaiClicker()
    plan = Plan()

    # Установка плана для фарма
    #plan.add(ChallengeType.SEPAL_GOLD, BaseMaterial.TREASURE_BUD, 1)
    #plan.add(ChallengeType.SEPAL_GOLD, BaseMaterial.MEMORIES_BUD, 1)
    plan.add(ChallengeType.CORROSION_CAVE, CorrosionCaveChallenge.DELUSION_PATH, 10)

    try:
        clicker.start_game(GAME_EXECUTABLE)
        clicker.login()

        plan_performer = PlanPerformer(clicker, plan)
        plan_performer.execute()
    except RuntimeError as error:
        logging.error(error)
    except:
        logging.error(traceback.format_exc())

    clicker.kill_game()
