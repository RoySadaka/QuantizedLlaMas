from dataclasses import dataclass
from typing import Optional

@dataclass
class Model:
    name:str
    path:str
    n_ctx:int
    n_gqa:Optional[int] # FOR LLAMA2-70B
    n_threads:int
    n_gpu_layers:int
    prompt_format:str