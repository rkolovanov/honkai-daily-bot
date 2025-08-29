from HonkaiClicker import HonkaiClicker
from PlanPerformer import Plan, PlanPerformer
from Types import *
import configparser
import ctypes
import elevate
import logging
import sys
import traceback


logger = logging.getLogger("main")


def init_config():
    config_path = "data/config.ini"
    config = configparser.ConfigParser()

    config.read(config_path)

    if not config.has_section("hsr"):
        config.add_section("hsr")

    if not config.has_option("hsr", "executable_path"):
        config.set("hsr", "executable_path", "S:\Games\Star Rail Games\StarRail.exe")

    with open(config_path, "w") as file:
        config.write(file)

    return config


def create_farm_plan() -> Plan:
    plan = Plan()

    # Farm plan setup
    #plan.add_battle_task(TaskType.SEPAL_GOLD, BaseMaterial.TREASURE_BUD, 2)
    #plan.add_battle_task(TaskType.CORROSION_CAVE, CorrosionCaveChallenge.DELUSION_PATH, 7)
    #plan.add_task(TaskType.ASSIGNMENTS)
    plan.add_task(TaskType.NAMELESS_HONOR)
    #plan.add_task(TaskType.AWARDS_COLLECTION)

    return plan


def main():
    config = init_config()
    clicker = HonkaiClicker(config.get("hsr", "executable_path"))
    plan = create_farm_plan()
    plan_performer = PlanPerformer(clicker, plan)

    try:
        clicker.start_game()
        clicker.login()
        plan_performer.execute()
    except:
        clicker.kill_game()
        raise

    clicker.kill_game()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            logger.info("Requesting admin rights...")
            elevate.elevate()
        else:
            main()
    except Exception as ex:
        logger.error(ex)
    except:
        traceback.format_exc()
