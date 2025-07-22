import os
import json

from renderer import prompt_all_pages_independent_report
from gpt_helper import points_about_element_in_factor_report

def build_report(factor_list, image_type: str) -> list:
    report = []
    for factor in factor_list:
        data = {}

        if factor == "Career_Interest":
            data["factor"] = "Interest"
        else:
            data["factor"] = factor.replace("_", " ")

        data["path"] = f"charts/{factor}/{image_type}.png"

        report.append(data)
    return report

def get_subject_mapped(subjects):
    SUBJECT_ACRONYMS = {
        "English": "E",
        "Physics": "P",
        "Chemistry": "C",
        "Biology": "B",
        "Economics": "En",
        "Mathematics": "M",
        "Physical Education": "Pe",
        "Computer Science": "Cs",
        "Home Science": "Hs",
        "Informatics Practices": "I",
        "Psychology": "Py",
        "Sociology": "So",
        "Geography": "G",
        "Legal Studies": "L",
        "Music": "Mu",
        "Fine Arts": "F"
    }

    acronyms = [SUBJECT_ACRONYMS.get(subject) for subject in subjects if subject in SUBJECT_ACRONYMS]
    return "|".join(acronyms)

def map_subject_to_score(subject_names, subject_score):
    data = {}
    for subject in subject_names:
        data[subject] = subject_score[subject]

    return data


def stream_reccomendation_function(stream_data, subject_data):
    # print(json.dumps(stream_data, indent = 2))
    # print(json.dumps(subject_data, indent = 2))

    stream_scores = [
        ("Science", stream_data["Science"][0]["average_score"]),
        ("Commerce", stream_data["Commerce"][0]["average_score"]),
        ("Humanities", stream_data["Humanities"][0]["average_score"])
    ]

    # Sort streams by score in descending order
    ranked_streams = [stream for stream, _ in sorted(stream_scores, key=lambda x: x[1], reverse=True)]

    print(ranked_streams[0])

    stream_reccomendation = {}

    stream_reccomendation["1"] = {
        "stream" : ranked_streams[0],
        "subject_mapping" : get_subject_mapped(stream_data[ranked_streams[0]][0]["subjects"]),
        "recomendation_text" : "(Recommendation Stream - 1)",
        "subject_score" : map_subject_to_score(stream_data[ranked_streams[0]][0]["subjects"], subject_data)
    }
    stream_reccomendation["2"] = {
        "stream" : ranked_streams[0],
        "subject_mapping" : get_subject_mapped(stream_data[ranked_streams[0]][1]["subjects"]),
        "recomendation_text" : "(Recommendation Stream - 2)",
        "subject_score" : map_subject_to_score(stream_data[ranked_streams[0]][1]["subjects"], subject_data)
    }
    stream_reccomendation["3"] = {
        "stream" : ranked_streams[1],
        "subject_mapping" : get_subject_mapped(stream_data[ranked_streams[1]][0]["subjects"]),
        "recomendation_text" : "(Recommendation Stream - 3)",
        "subject_score" : map_subject_to_score(stream_data[ranked_streams[1]][0]["subjects"], subject_data)
    }
    stream_reccomendation["4"] = {
        "stream" : ranked_streams[2],
        "subject_mapping" : get_subject_mapped(stream_data[ranked_streams[2]][1]["subjects"]),
        "recomendation_text" : "(Challenging - Will need more work)",
        "subject_score" : map_subject_to_score(stream_data[ranked_streams[2]][1]["subjects"], subject_data)
    }
    
    
    print(json.dumps(stream_reccomendation, indent = 2))


def make_composite_component(user_id, user_detail, user_report):
    print("hello from aptitude")
    with open("data/factor/Aptitude.json") as f:
        meta_data = json.load(f)

    factor_list = [
        "Career_Interest", "Aptitude", "Personality",
        "Learning_Style", "Basic_Values", "Work_Style",
        "Emotional_Intelligence"
    ]
    common_report = build_report(factor_list, "common")
    comperitive_bar_report = build_report(factor_list, "comperitive_bar")

    common_report_summary = [
        {
            "title": "Overview of Your Strengths",
            "content": (
                "At Auro.edu, we believe every student has a unique blend of strengths. "
                "This diagnostic report highlights those strengths and helps you understand where you excel."
            )
        },
        {
            "title": "Interest Report",
            "content": (
                "Your top interests lie in business, persuasive communication, and artistic fields, "
                "indicating your potential to thrive in creative, entrepreneurial, and leadership roles."
            )
        },
        {
            "title": "Aptitude Report",
            "content": (
                "Your strengths in mechanical, spatial, and numerical reasoning highlight your aptitude for analytical, "
                "technical, and problem-solving tasks, making you suited for careers that require precision and design thinking."
            )
        },
        {
            "title": "Personality Report",
            "content": (
                "With traits such as assertiveness, logical thinking, and a deliberate approach, you demonstrate "
                "confidence, grounded decision-making, and a thoughtful nature in addressing challenges."
            )
        },
        {
            "title": "Learning Style Report",
            "content": (
                "Your preference for visual learning, a self-paced environment, and deep mastery orientation shows "
                "you thrive in independent, flexible learning settings that allow for deeper understanding and self-direction."
            )
        },
        {
            "title": "Basic Values Report",
            "content": (
                "Your core values of autonomy, being mission-driven, and seeking stimulation guide your decisions, "
                "motivating you to pursue paths that offer independence, purpose, and dynamic challenges."
            )
        },
        {
            "title": "Work Style Report",
            "content": (
                "You excel in environments that are unpredictable, with a high need for independence and agility, "
                "allowing you to adapt and succeed in fast-paced, flexible settings that require quick thinking."
            )
        },
        {
            "title": "Emotional Intelligence Report",
            "content": (
                "Your self-regulation, motivation, and empathy show your ability to manage emotions and lead "
                "effectively, making you well-suited for personal and professional leadership."
            )
        },
        {
            "title": "Our View of You",
            "content": (
                "At Auro.edu, we see your potential for personal excellence and meaningful impact, and encourage "
                "you to explore paths that allow these strengths to thrive."
            )
        }
    ]

    stream_reccomendation = stream_reccomendation_function(user_report["streams"], user_report["subjects"])
    
    data = {
        "page_1": {
            "index": "8",
            "model_part_1": "Stream",
            "model_part_2": "Recommendation",
            "Factor": "Initial Report",
            "description" : """Initial Data Driven 7-Factor Model Analysis of Your Strengths and
                    Preferences for Tailored Stream Recommendations.""",
            "background_image": "images/cover/Aptitude.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence", "Stream Recommendation"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_4" : {
            "title" : "2. Summary Report",
            "paragraph" : """You are very strong in Business, Mechanical
                    Reasoning, Assertiveness, Visual Learning,
                    Autonomy, Unpredictability, and Self-
                    Regulation. These factors dominated the
                    results of your 7 diagnostic tests.""",
            "data" : common_report
        },
        "page_5" : {
            "data" : common_report_summary
        },
        "page_6" : {
            "title" : "2. Summary Report",
            "paragraph" : """You are very strong in Business, Mechanical
                    Reasoning, Assertiveness, Visual Learning,
                    Autonomy, Unpredictability, and Self-
                    Regulation. These factors dominated the
                    results of your 7 diagnostic tests.""",
            "data" : comperitive_bar_report
        },
        "page_7" : {
            "data" : common_report_summary
        },
        

    }

    # prompt_all_pages_independent_report(user_id, "Compo", data)


