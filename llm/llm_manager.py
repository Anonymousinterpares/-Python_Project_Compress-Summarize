import openai
import google.generativeai as genai
from PyQt5.QtWidgets import QMessageBox

def generate_llm_documentation(main_window, project_text):
    """Generates documentation using the selected LLM provider.
    Args:
        project_text (str): Project content to analyze
    Returns:
        str: Generated documentation text, or None if generation fails"""
    selected_llm = None
    if main_window.openai_radio.isChecked():
        selected_llm = "openai"
    elif main_window.google_radio.isChecked():
        selected_llm = "google"

    if not selected_llm:
        QMessageBox.warning(main_window, "Warning", "Please select an LLM provider.")
        return None

    llm_settings = main_window.api_settings.get(selected_llm, {})
    api_key = llm_settings.get("api_key")
    model = llm_settings.get("model")
    temperature = llm_settings.get("temperature", 0.7)

    if not api_key:
        QMessageBox.warning(main_window, "Error", f"{selected_llm.capitalize()} API key not configured.")
        return None

    overview_type = "general" if main_window.general_radio.isChecked() else "detailed"

    system_prompt = f"""You are a Coding Master tasked with explaining the provided code. Provide a {overview_type} overview. **Obligatory elements to be included: 1) Project Overview 2) Graphical Representation of project structure. 3) Functions 4) Dependencies**.
Do not comment on code issues, errors or potential for expansion. Provide a graphical overview of the project structure and main data flow using text characters. Use the following format as an example:
+-----------------+     +-----------------+     +-----------------+
| main.py   |---->| code1223445677899.py |---->| settings.json |
+-----------------+     +-----------------+     +-----------------+
      ^                                               |
      |                                               |
      +-----------------------------------------------+
                                         |
                                         V
                            +-----------------+
                            | PyQt5 library  |
                            +-----------------+"""

    if selected_llm == "openai":
        return call_openai_api(main_window, api_key, model, system_prompt, project_text, temperature)
    elif selected_llm == "google":
        return call_google_api(main_window, api_key, model, system_prompt, project_text, temperature)

def call_openai_api(main_window, api_key, model, system_prompt, content, temperature):
    """Makes a request to the OpenAI API for documentation generation.
    Args:
        api_key (str): OpenAI API key
        model (str): Model identifier
        system_prompt (str): System context for the request
        content (str): Project content to analyze
        temperature (float): Temperature setting for generation
    Returns:
        str: Generated content or None if request fails"""
    print(f"Calling OpenAI API with model: {model}, temperature: {temperature}")
    openai.api_key = api_key
    try:
        print(f"OpenAI API Request - Model: {model}, Temperature: {temperature}, Prompt: {system_prompt}, Content: {content[:500]}...")
        # Use openai.chat.completions.create for chat models
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=temperature,
        )
        print(f"OpenAI API Response: {response}")
        # Access the generated text from the response
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        QMessageBox.critical(main_window, "OpenAI Error", f"Error communicating with OpenAI: {e}")
        return None
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        QMessageBox.critical(main_window, "OpenAI Error", f"An unexpected error occurred with OpenAI: {e}")
        return None

def call_google_api(main_window, api_key, model, system_prompt, content, temperature):
    """Calls the Google API to generate documentation."""
    print(f"Calling Google API with model: {model}, temperature: {temperature}")
    genai.configure(api_key=api_key)
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=8192
    )
    if model.startswith("models/"):
        gemini_model = genai.GenerativeModel(model_name=model,
                                        generation_config=generation_config)
    else:
        gemini_model = genai.GenerativeModel(model, generation_config=generation_config)

    prompt = f"{system_prompt}\n\n{content}"
    print(f"Google API Request - Model: {model}, Temperature: {temperature}, Prompt: {prompt[:500]}...")
    try:
        response = gemini_model.generate_content(prompt)
        print(f"Google API Response: {response.text}")
        return response.text
    except Exception as e:
        print(f"Error calling Google API: {e}")
        QMessageBox.critical(main_window, "Google AI Error", f"Error communicating with Google AI: {e}")
        return None
