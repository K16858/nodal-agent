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
            
    def get_agent_context(self, agent_name: str) -> Optional[Dict]:
        if agent_name not in self.agents:
            return None
        
        agent_state = self.agent_states[agent_name]
        current_location = self.locations[agent_state['location']]
        
        # 現在の場所にいるオブジェクトを取得
        objects_here = []
        for obj_name, obj_location in self.object_locations.items():
            if obj_location == agent_state['location']:
                objects_here.append(self.objects[obj_name])
        
        # 現在の場所にいる他のエージェントを取得
        other_agents = []
        for other_name, other_state in self.agent_states.items():
            if other_name != agent_name and other_state['location'] == agent_state['location']:
                other_agents.append(other_name)
        
        return {
            'agent_name': agent_name,
            'current_location': current_location,
            'objects_here': objects_here,
            'other_agents': other_agents,
            'current_time': self.time,
            'connected_locations': current_location.connections
        }
        
    def get_valid_actions(self, agent_name: str) -> List[ActionType]:
        if agent_name not in self.agents:
            return []
        
        agent_state = self.agent_states[agent_name]
        current_location = self.locations[agent_state['location']]
        
        valid_actions = current_location.base_actions.copy()
        
        # オブジェクトに対するアクションを追加
        for obj in current_location.objects:
            if obj in self.objects:
                valid_actions.extend(self.objects[obj].actions)
        
        return list(set(valid_actions))
        