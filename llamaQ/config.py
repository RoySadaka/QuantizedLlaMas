from llamaQ.model import Model


class Config:
    model_name_to_model = {
        'Wizard-Vicuna-30B-Uncensored': Model(name="Wizard-Vicuna-30B-Uncensored", path="./models/Vicuna/Wizard-Vicuna-30B-Uncensored.ggmlv3.q4_1.bin", n_ctx=1024, n_threads=16, n_gpu_layers=60),
        'llama-30b.ggmlv3': Model(name="llama-30b.ggmlv3", path="./models/LLaMa/llama-30b.ggmlv3.q4_1.bin", n_ctx=1024, n_threads=16, n_gpu_layers=60),
        'guanaco-33B.ggmlv3': Model(name="guanaco-33B.ggmlv3", path="./models/Guanaco/guanaco-33B.ggmlv3.q4_1.bin", n_ctx=1024, n_threads=16, n_gpu_layers=60),
        'Alpaca-Lora-30B.ggmlv3': Model(name="Alpaca-Lora-30B.ggmlv3", path="./models/Alpaca/Alpaca-Lora-30B.ggmlv3.q4_1.bin", n_ctx=1024, n_threads=16, n_gpu_layers=60),
        }
    MIN_TEMPERATURE = 0
    MAX_TEMPERATURE = 1
    MIN_TOKENS = 20
    MAX_TOKENS = 512