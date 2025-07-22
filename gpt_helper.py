import requests
import urllib.parse
import os
import openai
import fitz  # Correct import
import json
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def hit_gpt(user_id, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
            cleaned_response = json.loads(response["choices"][0]["message"]["content"])
            return cleaned_response

        except json.JSONDecodeError:
            print(f"Retrying JSON parsing... Attempt {attempt + 1} of {retries}")
            print("erroe while solving for ", {user_id})
    return None


def points_about_element_in_factor_report(user_id, factor, Subfactor, Score):

    prompt = f"""For the subfactor [{Subfactor}] under [{factor}], assume my score is [{Score} %]. 
    I want a detailed paragraph in 80-90 words explaining what this score means for me. 
    Make the tone [analytical] and [personalised], and include how this could show up in real career roles. 
    Then give me a summary in bullet points with 3-4 lines. 
    Keep the summary short and to the point. Bold the important words in summary points use html tags to do this such that it injects in html
    
    Example Output Format (for factor: Basic Values and subfactor: Autonomy):
    {{
        "element_para": "You value freedom, independence, and self-direction. You are motivated when you're trusted to explore your own methods, ideas, and timelines. Micromanagement or highly restrictive environments may feel limiting to you. You're well-suited for entrepreneurial roles, research-driven fields, or creative industries where autonomy is not just accepted—but expected.",
        "meaning_for_you": [
            "You thrive when given space to make your own decisions.",
            "You prefer roles where you're accountable for outcomes, not just tasks",
            "You may struggle in overly rule-bound or hierarchical settings"
        ]
    }}
    """
    print("gettting gpt data for factor: ", factor, "element: ", Subfactor)


    dummy = {
        "element_para": "You value freedom, independence, and self-direction. You are motivated when you're trusted to explore your own methods, ideas, and timelines. Micromanagement or highly restrictive environments may feel limiting to you. You're well-suited for entrepreneurial roles, research-driven fields, or creative industries where autonomy is not just accepted—but expected.",
        "meaning_for_you": [
            "You thrive when given space to make your own decisions.",
            "You prefer roles where you're accountable for outcomes, not just tasks",
            "You may struggle in overly rule-bound or hierarchical settings"
        ]
    }

    return dummy

    return hit_gpt(user_id, prompt)
