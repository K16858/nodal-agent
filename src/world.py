import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from models import Object, LocationNode, WorldDefinition, ActionType
from agent import Agent

class World:
    def __init__(self, world_path: str):
        with open(world_path, 'r', encoding='utf-8') as f:
            world_data = json.load(f)
        world_def = WorldDefinition(**world_data)

        self.locations: Dict[str, LocationNode] = {loc.name: loc for loc in world_def.locations}
        self.objects: Dict[str, Object] = {obj.name: obj for obj in world_def.objects}
        self.agents: Dict[str, Agent] = {}
        
        self.agent_states: Dict[str, Dict] = {}
        
        self.time = 0
    
    def add_agent(self, agent: Agent, start_location: str):
        if start_location not in self.locations:
            raise ValueError(f"ロケーション：'{start_location}' は存在しません。")
        
        if agent.name in self.agents:
            raise ValueError(f"エージェント：'{agent.name}' はすでに存在します。")
        
        self.agents[agent.name] = agent
        self.agent_states[agent.name] = {
            'location': start_location,
        }
        
    def tick(self):
        self.time += 1
        if self.time > 96:
            self.time = 0
            
    
        