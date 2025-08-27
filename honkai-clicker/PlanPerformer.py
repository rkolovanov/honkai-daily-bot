from ChallengePerformer import *
from HonkaiClicker import HonkaiClicker
import logging


logger = logging.getLogger(__name__)


class Plan:
    def __init__(self):
        self.challenges = []

    def add(self, challenge_type: ChallengeType, resource: enum.Enum, number: int):
        challenge = Challenge(challenge_type, resource, number)
        self.challenges.append(challenge)


class PlanPerformer:
    def __init__(self, clicker: HonkaiClicker, plan: Plan):
        self._clicker = clicker
        self._plan = plan

    def _create_challenge_performer(self, challenge: Challenge):
        if challenge.challenge_type == ChallengeType.SEPAL_GOLD:
            return GoldSepalPerformer(self._clicker, challenge.resource)
        elif challenge.challenge_type == ChallengeType.CORROSION_CAVE:
            return CorrosionCavePerformer(self._clicker, challenge.resource)

        return None

    def execute(self):
        for challenge in self._plan.challenges:
            performer = self._create_challenge_performer(challenge)
            if performer is None:
                logger.error(f"Challenge '{challenge.challenge_type.name}' performer not implemented. Skipping...")
                continue

            performer.prepare()
            performer.execute(challenge.number)
