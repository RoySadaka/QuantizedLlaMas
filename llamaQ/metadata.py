from typing import Dict, List
from llamaQ.config import Config

class Metadata:
    system_role:str            = None
    conversation: List[str]    = ['']
    config = Config()
    chosen_model = None