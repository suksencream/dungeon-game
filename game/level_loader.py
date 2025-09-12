# game/level_loader.py
import json
import os
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

GridPos = Tuple[int, int]

@dataclass
class EnemySpawn:
    pos: GridPos
    speed: float
    patrol: List[GridPos]  # optional patrol points (can be empty)

@dataclass
class Level:
    width: int
    height: int
    tiles: List[List[int]]  # 0 = floor, 1 = wall
    player_start: GridPos
    exit_pos: GridPos
    enemies: List[EnemySpawn]
    jelly_count: int  # optional collectibles per level (for flavor)

def load_level(level_path: str) -> Level:
    with open(level_path, "r") as f:
        data: Dict[str, Any] = json.load(f)

    width = data["width"]
    height = data["height"]
    tiles = data["tiles"]
    player_start = tuple(data["player_start"])
    exit_pos = tuple(data["exit_pos"])
    jelly_count = data.get("jelly_count", 0)

    enemies = []
    for e in data.get("enemies", []):
        enemies.append(EnemySpawn(
            pos=tuple(e["pos"]),
            speed=float(e.get("speed", 2.0)),
            patrol=[tuple(p) for p in e.get("patrol", [])]
        ))

    return Level(
        width=width,
        height=height,
        tiles=tiles,
        player_start=player_start,
        exit_pos=exit_pos,
        enemies=enemies,
        jelly_count=jelly_count,
    )

def level_path_for(index: int) -> str:
    # 1 => level01.json
    here = os.path.dirname(__file__)
    fname = f"levels/level{index:02d}.json"
    return os.path.join(here, fname)
