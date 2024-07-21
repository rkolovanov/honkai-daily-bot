from HonkaiClicker import HonkaiClicker, Challenge, ChallengeType, ResourceType
import time


if __name__ == "__main__":
    clicker = HonkaiClicker()

    try:
        clicker.start_game("S:\Games\Star Rail\Games\StarRail.exe")
        clicker.login()

        challenge = Challenge(ChallengeType.SEPAL_GOLD, ResourceType.MONEY, 3)
        clicker.accomplish_challenge(challenge)
        time.sleep(3.0)

        challenge = Challenge(ChallengeType.SEPAL_GOLD, ResourceType.CHARACTER_EXP, 4)
        clicker.accomplish_challenge(challenge)
        time.sleep(3.0)

        challenge = Challenge(ChallengeType.SEPAL_GOLD, ResourceType.WEAPON_EXP, 1)
        clicker.accomplish_challenge(challenge)
        time.sleep(3.0)

    except Exception as error:
        print(error)

    clicker.kill_game()
