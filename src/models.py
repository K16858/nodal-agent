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
    portabel: bool
    actions: List[ActionType]

class LocationNode(BaseModel):
    name: str
    description: str
    objects: List[str] = []
    base_actions: List[ActionType]
    connections: List[str]

class WorldDefinition(BaseModel):
    locations: List[LocationNode]
    objects: List[Object]
