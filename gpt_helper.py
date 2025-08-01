import requests
import urllib.parse
import os
import openai
import fitz  # Correct import
import json
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import re

# Load variables from .env file
load_dotenv()

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
corcel_api_key = os.getenv("CORCEL_API_KEY")

def extract_clean_json(content):
    # First, remove code fencing if present
    if content.startswith("```json"):
        content = content[len("```json"):].strip()
    elif content.startswith("```"):
        content = content[len("```"):].strip()

    # Then, use regex to extract the JSON object
    match = re.search(r'(\{.*\})', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print("❌ JSON parse error after regex:", e)
            print("Offending content:\n", match.group(1))
    else:
        print("❌ No valid JSON found in response.")
    return None

def hit_gpt(user_id, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
            content = response["choices"][0]["message"]["content"].strip()

            cleaned_response = extract_clean_json(content)
            if cleaned_response:
                return cleaned_response

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}") 
            print(f"Retrying JSON parsing... Attempt {attempt + 1} of {retries}")
            print("erroe while solving for ", {user_id})
    return None

def hit_corcel(user_id, prompt):
    url = "https://api.corcel.io/v1/chat/completions"

    payload = {
        "model": "llama-3",
        "temperature": 0.1,
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": corcel_api_key
    }

    print("error before response")

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("raw response")
        # print(json.dumps(response.json(), indent=2))  # Better than printing raw text

        print("cleaned response")
        response_json = response.json()

        if "choices" in response_json and response_json["choices"]:
            content = response_json["choices"][0]["message"]["content"]
            try:
                cleaned_response = json.loads(content)  # Assuming the content is a JSON string
            except json.JSONDecodeError:
                cleaned_response = content  # It's plain text, not a JSON string

            # print(json.dumps(cleaned_response, indent=2) if isinstance(cleaned_response, dict) else cleaned_response)
            return cleaned_response
        else:
            print("No choices found in response.")
            return None

    except Exception as e:
        print(f"Exception occurred: {e}")
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

    # return dummy

    # return hit_corcel(user_id, prompt)
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

    dummy = {
            "high": "<Your high-level recommendation>",
            "medium": "<Your medium-level recommendation>",
            "low": "<Your low-level recommendation>"
        }
    # return dummy

    return hit_gpt(user_id, prompt)

def get_report_summary(user_id, factor):
    prompt = f"""
        based on the given data of user score give me 20-30 words summary of each factor, take example as the type of responce i am expecting
        imput data : 
        {
            {
                "factor" : factor
            }
        }

        output format:
        {{
            "one line summary" : "You are very strong in Business, Mechanical Reasoning, Assertiveness, Visual Learning, Autonomy, Unpredictability, and Self-Regulation. These factors dominated the results of your 7 diagnostic tests.",
            "overview" : "At Auro.edu, we believe every student has a unique blend of strengths. This diagnostic report highlights those strengths and helps you understand where you excel."
            "factor" : [
                {{
                "factor" : "Aptitude",
                "summary" : "Your strengths in mechanical, spatial, and numerical reasoning highlight your aptitude for analytical, technical, and problem-solving tasks, making you suited for careers that require precision and design 60% thinking."
                }}
            ],
            "our_overview_of_you": "At Auro.edu, we see your potential for personal excellence and meaningful impact, and encourage you to explore paths that allow these strengths to thrive."
        }}
    """

    return hit_gpt(user_id, prompt)

def get_comparision_summary(user_id, factor):
    prompt = f"""
        based on the given data of user score give me 15-25 words summary of each factor, take example as the type of responce i am expecting
        imput data : 
        {
            {
                "factor" : factor
            }
        }

        output format:
        {{
            "one line summary" : "Compared to your peers, you show higher creativity, business potential, and technical ability, and you thrive more in independent, hands-on, and flexible learning environments.",
            "Benchmarking Your Strengths" : "To help you better understand your strengths, the following section compares your scores with global averages, minimums, and maximums across each area."
            "factor" : [
                {{
                "factor" : "Personality",
                "summary" : "You show high assertiveness and emotional sensitivity, standing out from peers. Scores suggest strong independence but lower preference for teamwork and emotional resilience."
                }}
            ],
            "Our View of You": "At Auro.edu, we see you as an independent, driven learner with strong creative, spatial, and emotional strengths. We encourage you to pursue paths that align with your autonomy, curiosity, and desire for purpose-driven impact"
        }}
    """

    return hit_gpt(user_id, prompt)

    

def stream_recomendation_depth_explanation(user_id, stream_data, factor, goal, page_no):
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
        "recommendation_point": {{
            "1": "English, Physics, Chemistry, Mathematics, and Economics – is ideal for your high mechanical (92), numerical (85), and spatial (88) aptitudes, and your strong interest in business (92) and persuasion (88). This blend supports analytical thinking and opens up paths in technology, finance, and business innovation, where your skills can truly thrive.",
            "2": "..."
        }},
        "table_data": [
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
        "recommendation_point": {
            "1": "English, Physics, Chemistry, Mathematics, and Economics – is ideal for your high mechanical (92), numerical (85), and spatial (88) aptitudes, and your strong interest in business (92) and persuasion (88). This blend supports analytical thinking and opens up paths in technology, finance, and business innovation, where your skills can truly thrive.",
            "2": "..."
        },
        "table_data": [
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
    print("getting recomendation data for page no. ", page_no)
    # return dummy

    # return hit_corcel(user_id, prompt)

    return hit_gpt(user_id, prompt)

def stream_intrest_alinment_explanation(user_id, stream_data, factor, page_no):
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

    Here is the input data (as JSON):
    ```json
    {{
        "stream_data": {json.dumps(stream_data)},
        "career_interest": {json.dumps(factor)}
    }}

    Now, return ONLY this structure as raw JSON:
    {{
        "Interest Alignment": [
            {{
                "Factor": "Business",
                "score": "92",
                "Connection_To_Subject": "Economics, Math, Physics (Technology)",
                "fit": "Excellent"
            }}
            ],
        "Top_Career_Path": "Based on your profile, these science-related roles offer the right mix of analytical challenge, practical
                application, business strategy, and innovation potential",
        "stream_order": [
            {{
                "heading": "Subject Combination 1: HIS|POL|ECO",
                "Small text": "Ideal for roles that combine...",
                "jobs": [
                    {{
                    "job": "Data Scientist",
                    "reason": "using algorithms and data for prediction and analysis"
                    }}
                ]
            }},
            {{
                "heading": "Subject Combination 2: Ma|Go|Ec",
                "Small text": "Ideal for roles that combine...",
                "jobs": [
                    {{
                    "job": "Data Scientist",
                    "reason": "using algorithms and data for prediction and analysis"
                    }}
                ]
            }}
            ]
    }}
    """
    print("gettting intrest alinment data for page no. ", page_no)
    # return hit_corcel(user_id, prompt)
    # return "hi"
    return hit_gpt(user_id, prompt)

def subject_stream_analysis(user_id, stream_data, factor):
    prompt = f"""
        I have a diagnostic test. It contains 7 factors. Each factor has some weightage.

        Each factor has some subfactors. Students get scores in each subfactor through the diagnostic test. Based on these scores and the weightage of each factor, stream and subject combinations for Class 11 are recommended.

        I will give you all the necessary data—factor names, their weightage, each subfactor within a factor, students' scores in each subfactor, and the final recommendations.

        Now you need to create a paragraph for each factor, showing how individual scores in relevant subfactors and the weightage contributed to the final stream and subject recommendation.

        addinally give fit summary of each stream (where stream with index 1 is best fit and 4 least)
        and give a conclusion point

        Here is the data:
        {
            {
            "factor_data": factor,
            "stream_data" : stream_data
            }
        }

        output format only json: 
        {
            {
            "data" : [
                {
                    "factor" : "factor_name",
                    "paragraph" : "..."
                },
                {...}
            ],
            "table" : [
                {
                    "stream" : "Science + E|P|C|En|M",
                    "fit_summary" : "High cognative fit + business acumen + stratigic reasoning"
                },
                {...},
                {...},
                {
                    "stream" : "Avoid + Co|Ac|Bu|En|M",
                    "fit_summary" : "Overall theoretical, doesnt engage your strongest skills or motivation"
                }
            ],
            "Conclusion": "Your final recommendations were chosen not just by subject popularity, but by how strongly each subject engages your top cognitive strengths (like 92 in mechanical), emotional values (88 in autonomy), and motivation (92 in business + 88 in persuasion). This personalized blend ensures both academic excellence and long-term career alignment."
            }
        }

        Keep each paragraph about the factor in 70 - 100 words.
        """
    
    responce = {"data" : [
      {
        "factor": "Career Interest",
        "paragraph": "Scores in Career Interest like Artistic (85) and Business (92) strongly suggest a Commerce stream. High scores in Literary and Social also align with subjects like English and Legal Studies, influencing the recommendation for Commerce with subjects like Accountancy and Business Studies."
      },
      {
        "factor": "Aptitude",
        "paragraph": "High scores in Spatial (88) and Mechanical (92) aptitudes align with Science stream recommendations, particularly Physics and Chemistry. Numerical (85) and Verbal (67) support Commerce, influencing subjects like Mathematics and Economics."
      },
      {
        "factor": "Personality",
        "paragraph": "Assertiveness (85) and Factual Orientation (Thinking) (83) suggest a fit for leadership roles in Commerce. Lower scores in Team Orientation (Independent) (50) and Emotional stability (Sensitivity) (60) hint at potential challenges in group-oriented or high-pressure subjects."
      },
      {
        "factor": "Learning Style",
        "paragraph": "A dominant Visual + Kinesthetic learning style (90) supports subjects requiring practical and visual learning, like Chemistry and Physics in Science. High scores in Self-paced learning (78) and Deep Mastery (75) further align with detailed, self-driven study environments."
      },
      {
        "factor": "Basic Values",
        "paragraph": "High scores in Work Orientation (Experimentation) (85) and Decision Making (Autonomy) (92) suggest a preference for dynamic and autonomous work environments, aligning with subjects like Political Science and Economics in Humanities."
      },
      {
        "factor": "Work Style",
        "paragraph": "Preferences for Unpredictable tasks (92) and Higher Independence (88) suggest a good fit for subjects that require innovative thinking and self-direction, such as Political Science and Sociology in Humanities."
      },
      {
        "factor": "Emotional Intelligence",
        "paragraph": "Strong Emotional Intelligence, with high scores in Self-Regulation (92) and Motivation (88), supports roles requiring resilience and leadership, influencing recommendations towards Commerce and subjects like Business Studies and Economics."
      }
    ]
  }
    # return "hi"
    # return responce
    return hit_gpt(user_id, prompt)