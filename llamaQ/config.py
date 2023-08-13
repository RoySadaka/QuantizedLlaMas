from llamaQ.model import Model

# Llama2 70b must set the n_gqa parameter (grouped-query attention factor) to 8 when loading

class Config:
    default_prompt_template = '### Instruction:\n{}\nInput:\n{}\n### Response:\n{}'
    model_name_to_model = {
        'Wizard-Vicuna-30B-Uncensored': Model(name="Wizard-Vicuna-30B-Uncensored", path="./models/Vicuna/Wizard-Vicuna-30B-Uncensored.ggmlv3.q4_1.bin", n_ctx=1024, n_gqa=None, n_threads=16, n_gpu_layers=60, prompt_format=default_prompt_template),
        'llama-30b': Model(name="llama-30b", path="./models/LLaMa/llama-30b.ggmlv3.q4_1.bin", n_ctx=1024, n_gqa=None, n_threads=16, n_gpu_layers=60, prompt_format=default_prompt_template),
        'guanaco-33B': Model(name="guanaco-33B", path="./models/Guanaco/guanaco-33B.ggmlv3.q4_1.bin", n_ctx=1024, n_gqa=None, n_threads=16, n_gpu_layers=60, prompt_format=default_prompt_template),
        'Alpaca-Lora-30B': Model(name="Alpaca-Lora-30B", path="./models/Alpaca/Alpaca-Lora-30B.ggmlv3.q4_1.bin", n_ctx=1024, n_gqa=None, n_threads=16, n_gpu_layers=60, prompt_format=default_prompt_template),
        'Lazarus-30B': Model(name="Lazarus-30B", path="./models/Lazarus/30b-Lazarus.ggmlv3.q4_1.bin", n_ctx=1024, n_gqa=None, n_threads=16, n_gpu_layers=60, prompt_format=default_prompt_template),
        'Llama-2-13b-chat': Model(name="Llama-2-13b-chat", path="./models/LLaMa/llama-2-13b-chat.ggmlv3.q8_0.bin", n_ctx=4096, n_gqa=None, n_threads=16, n_gpu_layers=43, prompt_format='System: {}\nUser: {}\nAssistant: {}'),
        'Llama-2-13b': Model(name="Llama-2-13b", path="./models/LLaMa/llama-2-13b.ggmlv3.q8_0.bin", n_ctx=4096, n_gqa=None, n_threads=16, n_gpu_layers=43, prompt_format='System: {}\nUser: {}\nAssistant: {}'),
        'Llama-2-70b-chat': Model(name="Llama-2-70b-chat", path="./models/LLaMa/llama-2-70b-chat.ggmlv3.q5_0.bin", n_ctx=4096, n_gqa=8, n_threads=16, n_gpu_layers=32, prompt_format='System: {}\nUser: {}\nAssistant: {}'),
        'platypus2-70b': Model(name="platypus2-70b", path="./models/Platypus/platypus2-70b-instruct.ggmlv3.q4_K_M.bin", n_ctx=4096, n_gqa=8, n_threads=16, n_gpu_layers=38, prompt_format='### Instruction:\n{}\nInput:\n{}\n### Response:\n{}'),
        }
    MIN_TEMPERATURE = 0
    MAX_TEMPERATURE = 1
    MIN_TOKENS = 20
    MAX_TOKENS = 512