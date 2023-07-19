from llama_cpp import Llama, llama_free
from llamaQ.metadata import Metadata
from llamaQ.model import Model
from llamaQ.config import Config

def get_available_models(config: Config):
    return list(config.model_name_to_model.keys())

def load_model(model: Model) -> Llama:
    return Llama(model_path=model.path, n_ctx=model.n_ctx, n_threads=model.n_threads, n_gpu_layers=model.n_gpu_layers, verbose=False)

def unload_model(llama: Llama):
    llama_free(llama.ctx)

def token_count(llama: Llama, text: str):
    tokens = llama.tokenize(text.encode(encoding='utf-8'))
    return max(0, len(tokens) - 1)

def call_llm(metadata:Metadata, llm_model: Llama, system, user, assistant_guide, temperature, max_tokens, stop_sequence):
    config = metadata.config
    model_name = metadata.chosen_model
    prompt_format = config.model_name_to_model[model_name].prompt_format
    llm_input = prompt_format.format(system,user,assistant_guide)
    temperature = min(config.MAX_TEMPERATURE, max(temperature,config.MIN_TEMPERATURE))
    max_tokens = min(config.MAX_TOKENS, max(max_tokens, config.MIN_TOKENS))
    stop_sequence = stop_sequence if len(stop_sequence) > 0 else []

    out = llm_model(prompt=llm_input,
                max_tokens=max_tokens,
                stop=stop_sequence,
                temperature=temperature)
 
    generated_result = out['choices'][0]['text'].strip()
    stop_sequence_ending = stop_sequence if type(stop_sequence) == str else ''
    return generated_result + stop_sequence_ending