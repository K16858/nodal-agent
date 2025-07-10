from pydantic import BaseModel
from typing import List, Literal

ActionType = Literal[
    "move",      # 移動
    "take",      # 拾う
    "drop",      # 置く
    "examine",   # 調べる
    "use",       # 使う
    "talk",      # 話す
    "wait"       # 待機
]

class Object(BaseModel):
    name: str
    description: str
    protabel: bool
    actions: List[ActionType]

class LocationNode(BaseModel):
    name: str
    description: str
    objects: List[Object] = []
    base_actions: List[ActionType]
    connections: List[str]

class World(BaseModel):
    locations: List[LocationNode]
    objects: List[Object]
