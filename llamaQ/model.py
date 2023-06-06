from dataclasses import dataclass

@dataclass
class Model:
    name:str
    path:str
    n_ctx:int
    n_threads:int
    n_gpu_layers:int