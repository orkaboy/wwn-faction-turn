from src.goal import Goal
from src.mapper import get_class_values


class GOALS:
    """Static namespace for Example Goals."""

    BloodTheEnemy = Goal(
        name="Blood the Enemy",
        desc="Inflict a number of hit points of damage on enemy faction assets or bases equal to your faction's total Force, Cunning, and Wealth ratings.",  # noqa: E501
        difficulty=2,
    )

    DestroyTheFoe = Goal(
        name="Destroy the Foe",
        desc="Destroy a rival faction. Difficulty equal to 2 plus the average of the faction's Force, Cunning, and Wealth ratings.",  # noqa: E501
        difficulty=2,
    )

    EliminateTarget = Goal(
        name="Eliminate Target",
        desc="Choose an undamaged rival Asset. If you destroy it within three turns, succeed at a Difficulty 1 goal. If you fail, pick a new goal without suffering the usual turn of paralysis.",  # noqa: E501
        difficulty=1,
    )

    ExpandInfluence = Goal(
        name="Expand Influence",
        desc="Plant a Base of Influence at a new location. Difficulty 1, +1 if a rival contests it.",  # noqa: E501
        difficulty=1,
    )

    InsideEnemyTerritory = Goal(
        name="Inside Enemy Territory",
        desc="Have a number of Stealthed assets in locations where there is a rival Base of Influence equal to your Cunning score. Units that are already Stealthed in locations when this goal is adopted don't count.",  # noqa: E501
        difficulty=2,
    )

    InvincibleValor = Goal(
        name="Invincible Valor",
        desc="Destroy a Force asset with a minimum purchase rating higher than your faction's Force rating.",  # noqa: E501
        difficulty=2,
    )

    PeaceableKingdom = Goal(
        name="Peaceable Kingdom",
        desc="Don't take an Attack action for four turns.",
        difficulty=1,
    )

    RootOutTheEnemy = Goal(
        name="Root Out the Enemy",
        desc="Destroy a Base of Influence of a rival faction in a specific location. Difficulty equal to half the average of the current ruling faction's Force, Cunning, and Wealth ratings, rounded up.",  # noqa: E501
        difficulty=1,
    )

    SphereDominance = Goal(
        name="Sphere Dominance",
        desc="Choose Wealth, Force, or Cunning. Destroy a number of rival assets of that kind equal to your score in that attribute. Difficulty of 1 per 2 destroyed, rounded up.",  # noqa: E501
        difficulty=2,
    )

    WealthOfKingdoms = Goal(
        name="Wealth of Kingdoms",
        desc="Spend Treasure equal to four times your faction's Wealth rating on bribes and influence. This money is effectively lost, but the goal is then considered accomplished. The faction's Wealth rating must increase before this goal can be selected again.",  # noqa: E501
        difficulty=2,
    )


_goals = get_class_values(GOALS)


def goals_list() -> list[Goal]:
    """Return list of all Example Goals."""
    return _goals
