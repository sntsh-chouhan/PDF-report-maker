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

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}") 
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
    print("gettting gpt data for factor: ", factor, " and element: ", Subfactor)


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

def streat_overview(user_id, stream_reccomendation):
    prompt = f"""
    for the data {
        {
            "high" : stream_reccomendation["1"],
            "medium" : stream_reccomendation["3"],
            "low" : stream_reccomendation["4"]
        }
    }

    give me recomendation point based on the score of subjects in a given stream

    example of high level reccomendation : "These choices strongly align with your highest-scoring subjects—especially Physics, Chemistry, and
            Math—indicating a natural strength in analytical and structured thinking required for the Science stream."
    example of medium level reccomendation : "This stream leverages your strong abilities in Economics, English, and interdisciplinary subjects like
            Physics, offering a balanced path combining analytical thinking with communication and contextual
            reasoning."
    example of low level reccomendation : "Despite your good score in Math, low alignment in core commerce subjects like Accounts, Business, and
            Informatics suggests this stream may not suit your interest areas or natural aptitude"

    example_output : 
        Please respond in this format:
        {{
            "high": "<Your high-level recommendation>",
            "medium": "<Your medium-level recommendation>",
            "low": "<Your low-level recommendation>"
        }}
    """

    # print(prompt)
    dummy = {
            "high": "<Your high-level recommendation>",
            "medium": "<Your medium-level recommendation>",
            "low": "<Your low-level recommendation>"
        }
    return dummy
    return hit_gpt(user_id, prompt)

def stream_recomendation_depth_explanation(user_id, stream_data, factor, goal):
    # print(json.dumps(stream_data, indent= 2))
    # print(json.dumps(factor, indent= 2))
    prompt = f"""
    You are a career guidance AI that generates personalized academic stream recommendations based on user scores and psychological traits.

    ### Instructions:

    1. For each stream in the `stream_data`, write a highly personalized and analytical recommendation.
    2. Use the relevant **subject scores** and connect them with **psychological scores** from the `factors` dictionary (pick top 4)(like aptitude, interests, learning style, Professional Values, Personality,  and work style).
    3. The tone should be **insightful**, **personalized**, and **strategic**—as if giving guidance for a long-term academic decision.
    4. Highlight subjects, strengths, and psychological alignment with real reasoning.
    5. Mention score values where impactful (e.g., "your strong interest in Business (92) and aptitude in Mechanical reasoning (88)").
    6. The Goal of reccomendation is in three level (Best Suit, Can try, Should Ignore)

    imput_data : {
        {
            "stream_data": stream_data,
            "factor": factor,
            "goal": goal
        }
    }

    example Output format (JSON only):
    {{
        "recomendation_point": {{
            "1": "English, Physics, Chemistry, Mathematics, and Economics – is ideal for your high mechanical (92), numerical (85), and spatial (88) aptitudes, and your strong interest in business (92) and persuasion (88). This blend supports analytical thinking and opens up paths in technology, finance, and business innovation, where your skills can truly thrive.",
            "2": "..."
        }},
        "tabel_data": [
            {{
                "Factor" : "Aptitude",
                "Summary": "Exceptional Mechanical (92), Numerical (85), and Spatial (88) scores point toward subjects that involve problem-solving, logic, and precision—like Physics, Chemistry, Math, and Economics."
            }},
            {{
                "Factor" : "...",
                "Summary": "..."
            }}
        ]
    }}
    """

    dummy = {
        "recomendation_point": {
            "1": "English, Physics, Chemistry, Mathematics, and Economics – is ideal for your high mechanical (92), numerical (85), and spatial (88) aptitudes, and your strong interest in business (92) and persuasion (88). This blend supports analytical thinking and opens up paths in technology, finance, and business innovation, where your skills can truly thrive.",
            "2": "..."
        },
        "tabel_data": [
            {
                "Factor" : "Aptitude",
                "Summary": "Exceptional Mechanical (92), Numerical (85), and Spatial (88) scores point toward subjects that involve problem-solving, logic, and precision—like Physics, Chemistry, Math, and Economics."
            },
            {
                "Factor" : "...",
                "Summary": "..."
            }
        ]
    }
    return dummy

    return hit_gpt(user_id, prompt)

def stream_intrest_alinment_explanation(user_id, stream_data, factor):
    prompt = f"""
    1. Identify the Top 5 Career Interest areas by score in career_interest .

    2. For each:
    - Mention interest name and score.
    - Connect with 1–2 relevant school subjects.
    - Assign a fit level:
        Excellent: ≥90, Strong: 85–89, High: 75–84, Moderate: 60–74, Caution: <60

    3. Under "Top Career Paths for You":
    - From `stream_data`.
    - For each:
        - Show subject code (e.g., HIS|POL|ECO)
        - Add a 1-liner description of fit
        - Suggest 4–5 careers with brief reasoning

    imput_data : {
        {
            "stream_data": stream_data,
            "career_interest": factor,
        }
    }

    example Output format:
    {{
        "Interest Alignment": [
            {{
                "Factor" : "Buisness",
                "score" : "92",
                "Connection To Subject": "Economics, Physics (Practical), Math",
                "fit" : "Excellent"
            }}
        ],
        "Top_Career_Path" : "Based on your profile, these science-related roles offer the right mix of analytical challenge, practical application, business strategy, and innovation potential:",
        "stream_order" : [
            {{
                "heading" : "Subject Combination 1 : E|P|C|En|M",
                "Small text" : "Ideal for roles that combine science and commerce:",
                "jobs" : [
                    {{
                        "job" : "Data Scientist",
                        "reason" : "using algorithms and data for prediction and analysis"
                    }}
                ]
            }}
        ]
    }}
    """

    # print(prompt)

    return hit_gpt(user_id, prompt)