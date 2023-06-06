import gc
import gradio as gr
from llamaQ.app import app
import llamaQ.logic as lo

def get_all_elements():
    gr_elements = {e: gr.update(visible=True) for e in app.gr_elements}

    # UPDATE TOKEN COUNTER LABELS
    gr_elements[app.gr_token_counter_labels] = gr.update(value=app.token_counts_value, visible=True)

    # UPDATE RESULT TEXT
    gr_elements[app.gr_assistant] = gr.update(value=app.metadata.conversation[-1], visible=True)

    # UPDATE STATE AFTER MODEL WAS CHOSEN
    if app.metadata.chosen_model is not None:
        gr_elements[app.gr_token_counter_btn].update(interactive=True, visible=True)
        gr_elements[app.gr_run_btn].update(interactive=True, visible=True)
        gr_elements[app.gr_model_picker].update(interactive=False, visible=True)

    return gr_elements

def run_llama_handler(system, user, assistant_guide, temperature, max_tokens, stop_sequence):
    result = lo.call_llm(config=app.metadata.config, llm_model=app.llm, system=system, user=user, assistant_guide=assistant_guide, temperature=temperature, max_tokens=max_tokens, stop_sequence=stop_sequence)
    app.metadata.conversation = [system,user,assistant_guide+result]
    return get_all_elements()

def token_counter_handler(system, user, assistant_guide, assistant):
    system_count = lo.token_count(llama=app.llm, text=system)
    user_count = lo.token_count(llama=app.llm, text=user)
    assistant_guide_count = lo.token_count(llama=app.llm, text=assistant_guide)
    assistant_count = lo.token_count(llama=app.llm, text=assistant)
    total = system_count + user_count + assistant_guide_count + assistant_count
    # ESTIMATED SINCE THERE ARE THE LLAMA TEMPLATE TOKENS
    estimated_left_over_to_generate = app.llm.params.n_ctx - system_count - user_count - assistant_guide_count
    app.token_counts_value = [(str(system_count),"System"),(str(user_count),"User"),(str(assistant_guide_count),"Assistant Guide"),(str(assistant_count),"Assistant"),(str(total),"Total"),(str(estimated_left_over_to_generate),"Estimated left over to generate")]
    return get_all_elements()

def model_picker_handler(val):
    if app.metadata.chosen_model != val:
        if app.metadata.chosen_model is not None:
            print(f'Unloading model {app.metadata.chosen_model}...')
            lo.unload_model(app.llm)
            gc.collect()
        print(f'Loading model {val}...')
        app.metadata.chosen_model = val
        app.llm = lo.load_model(app.metadata.config.model_name_to_model[app.metadata.chosen_model])
    return get_all_elements()
    
def initialize():
    app.gr_elements = []

def run():
    initialize()

    # HEADER
    header = gr.Markdown("""
![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/llamas/banner.jpg)
<h1><center>Quantized LLaMas 🎛️ 🦙🦙🦙 🎛️ (Classifier edition)</center></h1>
<h3><center>Wield the impressive ability to accurately spit up to 10 feet away</center></h3>

---
""")

    app.gr_main_row = gr.Row().style(equal_height=True)
    app.gr_elements.append(app.gr_main_row)
    app.gr_main_cl1 = gr.Column(scale=2)
    app.gr_elements.append(app.gr_main_cl1)
    app.gr_main_cl2 = gr.Column(scale=3)
    app.gr_elements.append(app.gr_main_cl2)
    app.gr_main_cl3 = gr.Column(scale=1)
    app.gr_elements.append(app.gr_main_cl3)


    # ----- TOKEN COUNTER ----- #

    # ROW
    app.gr_token_counter_row = gr.Row().style(equal_height=True)
    app.gr_elements.append(app.gr_token_counter_row)
    app.gr_token_counter_cl1 = gr.Column(scale=5)
    app.gr_elements.append(app.gr_token_counter_cl1)
    app.gr_token_counter_cl2 = gr.Column(scale=1)
    app.gr_elements.append(app.gr_token_counter_cl2)
    
    # LABELS
    app.token_counts_value = [("0","System"),("0","User"),("0","Assistant Guide"),("0","Assistant"),("0","Total"),("0","Left over"),("0","Estimated left over to generate")]
    app.gr_token_counter_labels = gr.HighlightedText(label="Token counts", value=app.token_counts_value)
    app.gr_elements.append(app.gr_token_counter_labels)

    # COUNT BUTTON
    app.gr_token_counter_btn = gr.Button(value="Refresh count ↻", interactive=False, visible=True)
    app.gr_elements.append(app.gr_token_counter_btn)
    # ----- SETTINGS ----- #

    # MODEL PICKER
    app.gr_model_picker = gr.Dropdown(choices=lo.get_available_models(app.metadata.config), value=[lo.get_available_models(app.metadata.config)[0]], multiselect=False, label="Model", info="More models will come", interactive=True, visible=True)
    app.gr_elements.append(app.gr_model_picker)

    # TEMPERATURE
    app.gr_temperature_slider = gr.Slider(app.metadata.config.MIN_TEMPERATURE, app.metadata.config.MAX_TEMPERATURE, value=0, label="Temperature", info="Choose between 0 and 1", interactive=True, visible=True)
    app.gr_elements.append(app.gr_temperature_slider)

    # MAX TOKENS
    app.gr_max_tokens_slider = gr.Slider(app.metadata.config.MIN_TOKENS, app.metadata.config.MAX_TOKENS, value=100, label="Max tokens", info="Choose between 20 and 512", interactive=True, visible=True)
    app.gr_elements.append(app.gr_max_tokens_slider)

    # STOP SEQUENCE
    app.gr_stop_sequence = gr.Textbox(label='Stop sequence', placeholder="###",lines=1, interactive=True, visible=True)
    app.gr_elements.append(app.gr_stop_sequence)


    # ----- INFERENCE ----- #


    # SYSTEM PROMPT
    app.gr_system = gr.Textbox(label='SYSTEM', placeholder="You are a helpful assistant.",lines=2, visible=True) # 2 for multiline
    app.gr_elements.append(app.gr_system)

    # USER
    app.gr_user = gr.Textbox(label='USER', placeholder="Enter a user message here.",lines=2, visible=True) # 2 for multiline
    app.gr_elements.append(app.gr_user)

    # ASSISTANT
    app.gr_assistant_guide = gr.Textbox(label='ASSISTANT GUIDE', placeholder="{\"key\":", interactive=True, visible=True)
    app.gr_elements.append(app.gr_assistant_guide)

    # RUN BUTTON
    app.gr_run_btn = gr.Button(value="Run", interactive=False, visible=True)
    app.gr_elements.append(app.gr_run_btn)

    # ASSISTANT
    app.gr_assistant = gr.Textbox(label='ASSISTANT', placeholder="Results will be displayed here.", interactive=False, visible=True)
    app.gr_elements.append(app.gr_assistant)

    with gr.Blocks(analytics_enabled=False) as llamas:
        header.render()

        app.gr_token_counter_row.render()
        with app.gr_token_counter_row:

            app.gr_token_counter_cl1.render()
            with app.gr_token_counter_cl1:
                app.gr_token_counter_labels.render()
            app.gr_token_counter_cl2.render()
            with app.gr_token_counter_cl2:
                app.gr_token_counter_btn.render()
                app.gr_token_counter_btn.click(token_counter_handler, inputs=[app.gr_system, app.gr_user, app.gr_assistant_guide, app.gr_assistant], outputs=app.gr_elements)

        app.gr_main_row.render()
        with app.gr_main_row:

            app.gr_main_cl1.render()
            with app.gr_main_cl1:
                app.gr_system.render()

            app.gr_main_cl2.render()
            with app.gr_main_cl2:
                app.gr_user.render() 
                app.gr_assistant_guide.render()
                app.gr_run_btn.render()
                app.gr_run_btn.click(run_llama_handler, inputs=[app.gr_system, app.gr_user, app.gr_assistant_guide, app.gr_temperature_slider, app.gr_max_tokens_slider, app.gr_stop_sequence], outputs=app.gr_elements)
                app.gr_assistant.render()

            app.gr_main_cl3.render()
            with app.gr_main_cl3:
                app.gr_model_picker.render()
                app.gr_model_picker.change(fn=model_picker_handler, inputs=app.gr_model_picker, outputs=app.gr_elements)
                app.gr_temperature_slider.render()
                app.gr_max_tokens_slider.render()
                app.gr_stop_sequence.render()

    llamas.launch(share=True, show_api=False)
