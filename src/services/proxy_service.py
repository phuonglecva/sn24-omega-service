import random
import json
class ProxyService:
    def __init__(self) -> None:
        self.path = "proxies.json" 
        self.load_proxys()
    
    def load_proxys(self):  
        with open(self.path, "r") as f:
            self.proxys = json.load(f)
            
    def get_proxys(self) -> str:
        return self.proxys

    def get_random_proxy(self) -> str:
        return random.choice(self.proxys)
