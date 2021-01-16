from dataclasses import dataclass


@dataclass
class Score:
    """Количество очков набранное игроком на определенном уровне"""
    user: str
    score: int
    level: str
