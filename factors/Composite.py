import os
import json

from renderer import prompt_all_pages_composite_report
from gpt_helper import points_about_element_in_factor_report


def int_to_roman(n: int) -> str:
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman += syms[i]
            n -= val[i]
        i += 1
    return roman


def build_report(factor_list, image_type: str, base) -> list:
    report = []
    count = 1
    for factor in factor_list:
        data = {}

        if factor == "Career_Interest":
            factor_name = "Interest"
        else:
            factor_name = factor.replace("_", " ")

        roman_num = int_to_roman(count)
        data["factor"] = f"{roman_num}. {factor_name}"
        data["path"] = f"charts/{factor}/{image_type}.png"
        data["footer"] = f"Exibit {base}.{count}"

        report.append(data)
        count += 1
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
        "Fine Arts": "F",
    }

    acronyms = [
        SUBJECT_ACRONYMS.get(subject)
        for subject in subjects
        if subject in SUBJECT_ACRONYMS
    ]
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
        ("Humanities", stream_data["Humanities"][0]["average_score"]),
    ]

    # Sort streams by score in descending order
    ranked_streams = [
        stream for stream, _ in sorted(stream_scores, key=lambda x: x[1], reverse=True)
    ]

    stream_reccomendation = {}

    stream_reccomendation["1"] = {
        "stream": ranked_streams[0],
        "subject_mapping": get_subject_mapped(
            stream_data[ranked_streams[0]][0]["subjects"]
        ),
        "recommendation_text": "(Recommendation Stream - 1)",
        "subject_score": map_subject_to_score(
            stream_data[ranked_streams[0]][0]["subjects"], subject_data
        ),
    }
    stream_reccomendation["2"] = {
        "stream": ranked_streams[0],
        "subject_mapping": get_subject_mapped(
            stream_data[ranked_streams[0]][1]["subjects"]
        ),
        "recommendation_text": "(Recommendation Stream - 2)",
        "subject_score": map_subject_to_score(
            stream_data[ranked_streams[0]][1]["subjects"], subject_data
        ),
    }
    stream_reccomendation["3"] = {
        "stream": ranked_streams[1],
        "subject_mapping": get_subject_mapped(
            stream_data[ranked_streams[1]][0]["subjects"]
        ),
        "recommendation_text": "(Recommendation Stream - 3)",
        "subject_score": map_subject_to_score(
            stream_data[ranked_streams[1]][0]["subjects"], subject_data
        ),
    }
    stream_reccomendation["4"] = {
        "stream": ranked_streams[2],
        "subject_mapping": get_subject_mapped(
            stream_data[ranked_streams[2]][1]["subjects"]
        ),
        "recommendation_text": "(Challenging - Will need more work)",
        "subject_score": map_subject_to_score(
            stream_data[ranked_streams[2]][1]["subjects"], subject_data
        ),
    }

    # print(json.dumps(stream_reccomendation, indent = 2))


def make_composite_component(user_id, user_detail, user_report):
    print("hello from Composite")
    with open("data/factor/Aptitude.json") as f:
        meta_data = json.load(f)

    factor_list = [
        "Career_Interest",
        "Aptitude",
        "Personality",
        "Learning_Style",
        "Basic_Values",
        "Work_Style",
        "Emotional_Intelligence",
    ]
    common_report = build_report(factor_list, "common", 2)
    comperitive_bar_report = build_report(factor_list, "comperitive_bar", 3)

    common_report_summary = [
        {
            "title": "Overview of Your Strengths",
            "content": (
                "At Auro.edu, we believe every student has a unique blend of strengths. "
                "This diagnostic report highlights those strengths and helps you understand where you excel."
            ),
        },
        {
            "title": "Interest Report",
            "content": (
                "Your top interests lie in business, persuasive communication, and artistic fields, "
                "indicating your potential to thrive in creative, entrepreneurial, and leadership roles."
            ),
        },
        {
            "title": "Aptitude Report",
            "content": (
                "Your strengths in mechanical, spatial, and numerical reasoning highlight your aptitude for analytical, "
                "technical, and problem-solving tasks, making you suited for careers that require precision and design thinking."
            ),
        },
        {
            "title": "Personality Report",
            "content": (
                "With traits such as assertiveness, logical thinking, and a deliberate approach, you demonstrate "
                "confidence, grounded decision-making, and a thoughtful nature in addressing challenges."
            ),
        },
        {
            "title": "Learning Style Report",
            "content": (
                "Your preference for visual learning, a self-paced environment, and deep mastery orientation shows "
                "you thrive in independent, flexible learning settings that allow for deeper understanding and self-direction."
            ),
        },
        {
            "title": "Basic Values Report",
            "content": (
                "Your core values of autonomy, being mission-driven, and seeking stimulation guide your decisions, "
                "motivating you to pursue paths that offer independence, purpose, and dynamic challenges."
            ),
        },
        {
            "title": "Work Style Report",
            "content": (
                "You excel in environments that are unpredictable, with a high need for independence and agility, "
                "allowing you to adapt and succeed in fast-paced, flexible settings that require quick thinking."
            ),
        },
        {
            "title": "Emotional Intelligence Report",
            "content": (
                "Your self-regulation, motivation, and empathy show your ability to manage emotions and lead "
                "effectively, making you well-suited for personal and professional leadership."
            ),
        },
        {
            "title": "Our View of You",
            "content": (
                "At Auro.edu, we see your potential for personal excellence and meaningful impact, and encourage "
                "you to explore paths that allow these strengths to thrive."
            ),
        },
    ]

    stream_reccomendation = stream_reccomendation_function(
        user_report["streams"], user_report["subjects"]
    )

    data = {
        "page_1": {
            "index": "8",
            "model_part_1": "Stream",
            "model_part_2": "Recommendation",
            "Factor": "Initial Report",
            "description": """Initial Data Driven 7-Factor Model Analysis of Your Strengths and
                    Preferences for Tailored Stream Recommendations.""",
            "background_image": "images/cover/Aptitude.png",
            "factors": [
                "Interest",
                "Aptitude",
                "Personality",
                "Learning Styles",
                "Basic Values",
                "Work Style",
                "Emotional Intelligence",
                "Stream Recommendation",
            ],  # pass all factors in array only
            "user_detail": user_detail,
        },
        "page_4": {
            "title": "2. Summary Report",
            "paragraph": """You are very strong in Business, Mechanical
                    Reasoning, Assertiveness, Visual Learning,
                    Autonomy, Unpredictability, and Self-
                    Regulation. These factors dominated the
                    results of your 7 diagnostic tests.""",
            "data": common_report,
            "page_no.": "4",
            "page_display": "3",
        },
        "page_5": {"data": common_report_summary, "page_no.": "5", "page_display": "6"},
        "page_6": {
            "title": "2. Summary Report",
            "paragraph": """You are very strong in Business, Mechanical
                    Reasoning, Assertiveness, Visual Learning,
                    Autonomy, Unpredictability, and Self-
                    Regulation. These factors dominated the
                    results of your 7 diagnostic tests.""",
            "note": """*Note: The average, minimum, and maximum scores are
                    computed based on global student data for this test.""",
            "data": comperitive_bar_report,
            "page_no.": "6",
            "page_display": "7",
        },
        "page_7": {
            "data": common_report_summary,
            "page_no.": "7",
            "page_display": "8",
        },
        "page_8": {
            "data": {
                "1": {
                    "stream": "Humanities",
                    "stream_score": 584.4,
                    "subject_mapping": "HIS|Geo|Psy",
                    "recommendation_text": "(Recommendation Stream - 1)",
                    "subject_score": {
                        "English": 750,
                        "Fine Arts": 860,
                        "History": 713,
                        "Geography": 605,
                        "Psychology": 434,
                    },
                },
                "2": {
                    "stream": "Humanities",
                    "stream_score": 544.6,
                    "subject_mapping": "HIS|POL|ECO|Geo",
                    "recommendation_text": "(Recommendation Stream - 2)",
                    "subject_score": {
                        "English": 750,
                        "History": 713,
                        "Political Science": 865,
                        "Economics": 554,
                        "Geography": 605,
                    },
                },
                "3": {
                    "stream": "Science",
                    "stream_score": 540.4,
                    "subject_mapping": "Phy|Chem|Bio|CS",
                    "recommendation_text": "(Recommendation Stream - 3)",
                    "subject_score": {
                        "English": 750,
                        "Physics": 462,
                        "Chemistry": 669,
                        "Biology": 589,
                        "Computer Science": 712,
                    },
                },
                "4": {
                    "stream": "Commerce",
                    "stream_score": 392.5,
                    "subject_mapping": "ACC|BST|ECO|Math|MS",
                    "recommendation_text": "(Challenging - Will need more work)",
                    "subject_score": {
                        "English": 750,
                        "Accountancy": 697,
                        "Business Studies": 674,
                        "Economics": 554,
                        "Mathematics": 547,
                        "Music": 704,
                    },
                },
            },
            "points": {
                "high": "These choices strongly align with your highest-scoring subjects\u2014especially Fine Arts, History, and Geography\u2014indicating a natural strength in creative and analytical thinking required for the Humanities stream.",
                "medium": "This stream leverages your strong abilities in Computer Science, Chemistry, and Biology, offering a balanced path combining analytical thinking with scientific reasoning, suitable for the Science stream.",
                "low": "Despite your good score in Accountancy and Business Studies, lower alignment in core commerce subjects like Economics suggests this stream may challenge your interest areas or natural aptitude, requiring more effort to excel in the Commerce stream.",
            },
        },
        "page_9": {
            "stream": "Humanities",
            "title": "5. Subject and Stream Recommendation Analysis",
            "sub_title": "Stream Recommendation 1 & 2 : ",
            "color": "#10C70080",
            "meta_data": [
                {
                    "stream": "Humanities",
                    "stream_score": 584.4,
                    "subject_mapping": "HIS|Geo|Psy",
                    "recommendation_text": "(Recommendation Stream - 1)",
                    "subject_score": {
                        "English": 750,
                        "Fine Arts": 860,
                        "History": 713,
                        "Geography": 605,
                        "Psychology": 434,
                    },
                },
                {
                    "stream": "Humanities",
                    "stream_score": 544.6,
                    "subject_mapping": "HIS|POL|ECO|Geo",
                    "recommendation_text": "(Recommendation Stream - 2)",
                    "subject_score": {
                        "English": 750,
                        "History": 713,
                        "Political Science": 865,
                        "Economics": 554,
                        "Geography": 605,
                    },
                },
            ],
            "data": {
                "recommendation_point": [
                    "Your exceptional scores in English (750), Fine Arts (860), and History (713) align well with your artistic (85) and literary (80) interests, suggesting a strong fit for Humanities. The combination of your high scores in these subjects and your interest in social (80) and persuasive (88) activities indicates a potential for success in fields that require strong communication and understanding of cultural contexts. Additionally, your personality traits such as factual orientation (thinking) at 83 and assertiveness (assertive) at 85 support a career path where critical thinking and assertive communication are valued. This stream, focusing on History, Geography, and Psychology, leverages your strengths and aligns with your values of cultural alignment (respect for tradition) at 75 and work value (mission-driven) at 88.",
                    "Your high scores in English (750), History (713), and Political Science (865) complement your interests in business (92) and persuasive (88) activities, making this Humanities stream a strategic choice. The inclusion of Economics (554), despite being slightly lower, is supported by your numerical aptitude (85) and decision-making autonomy (92), suggesting potential for growth in this area. Your personality traits of assertiveness (85) and factual orientation (thinking) at 83, along with a strong work value (mission-driven) at 88, align well with the demands of Political Science and Economics, which require a clear understanding of complex systems and the ability to articulate and defend positions effectively.",
                ],
                "table_data": [
                    {
                        "Factor": "Aptitude",
                        "Summary": "High scores in Mechanical (92), Numerical (85), and Spatial (88) aptitudes suggest strong analytical and problem-solving skills, essential for subjects like Economics and Geography.",
                    },
                    {
                        "Factor": "Career Interest",
                        "Summary": "Strong interests in Business (92), Artistic (85), and Persuasive (88) activities align well with subjects like Political Science, Economics, and Fine Arts, supporting careers in areas such as advocacy, economic analysis, and creative industries.",
                    },
                    {
                        "Factor": "Personality",
                        "Summary": "Traits like Assertiveness (85) and Factual Orientation (Thinking) (83) are conducive to success in fields requiring strong leadership and critical analysis, such as Political Science and History.",
                    },
                    {
                        "Factor": "Professional Values",
                        "Summary": "High valuation of Mission-Driven work (88) and Cultural Alignment (Respect for Tradition) (75) suggest a strong fit for Humanities, particularly in roles that impact societal values and maintain cultural heritage.",
                    },
                ],
            },
            "page_no.": "7",
            "page_display": "8",
        },
        "page_10": {
            "data": {
                "Interest Alignment": [
                    {
                        "Factor": "Buisness",
                        "score": "92",
                        "Connection_to_subject": "Economics, Physics (Practical), Math",
                        "fit": "Excellent",
                    }
                ],
                "Top_Career_Path": "Based on your profile, these science-related roles offer the right mix of analytical challenge, practical application, business strategy, and innovation potential:",
                "stream_order": [
                    {
                        "heading": "Subject Combination 1 : E|P|C|En|M",
                        "Small text": "Ideal for roles that combine science and commerce:",
                        "jobs": [
                            {
                                "job": "Data Scientist",
                                "reason": "using algorithms and data for prediction and analysis",
                            }
                        ],
                    }
                ],
            },
                "page_no.": "8",
                "page_display": "9",
        },
        "page_15": {
            "heading": "4. Subject and Stream Recommendation Analysis",
            "paragraph": "Your stream recommendations are the outcome of a structured, evidence-based evaluation that\n                    integrates multiple dimensions of your profile\u2014aptitude scores, interest alignment, professional\n                    values, emotional drivers, and preferred learning style. Each component was assigned a weight as\n                    per our proprietary economic model, and their intersection revealed the most optimal academic\n                    paths for you.\n                    ",
            "points": [
                {
                    "factor": "Career Interest",
                    "paragraph": "High scores in Business (92) and Persuasive (88) align with Commerce, emphasizing strategic and communicative skills essential for this stream.",
                },
                {
                    "factor": "Aptitude",
                    "paragraph": "Strong Mechanical (92) and Spatial (88) aptitudes suggest proficiency in structured, logical tasks, supporting subjects like Mathematics and Physics.",
                },
                {
                    "factor": "Personality",
                    "paragraph": "Assertiveness (85) and Factual Orientation (Thinking) (83) indicate a decisive, pragmatic personality, fitting for Commerce and Economics.",
                },
                {
                    "factor": "Learning Style",
                    "paragraph": "Preference for Visual + Kinesthetic (90) learning aligns with active and engaging subjects like Business Studies and Economics.",
                },
            ],
        },
        "page_16": {
            "points": [
                {
                    "factor": "Basic Values",
                    "paragraph": "High Work Orientation (Experimentation) (85) and Decision Making (Autonomy) (92) support independent and innovative subject choices in Commerce.",
                },
                {
                    "factor": "Work Style",
                    "paragraph": "Independence (88) and Tasks - Unpredictable (92) suggest a fit for dynamic environments, aligning with subjects requiring strategic analysis.",
                },
                {
                    "factor": "Emotional Intelligence",
                    "paragraph": "High scores in Self-Regulation (92) and Motivation (88) are crucial for success in challenging subjects like Accountancy and Business Studies.",
                },
            ],
            "table": [
                {
                    "stream": "Commerce + En|Ac|Bs|Ec|Ma|Le",
                    "fit_summary": "Strong business acumen and strategic reasoning align with high scores in Business and Persuasive skills.",
                },
                {
                    "stream": "Commerce + En|Ac|Bs|Ec|Ma|Mu",
                    "fit_summary": "Similar to stream 1, with added creative outlet in Music, matching Artistic interests.",
                },
                {
                    "stream": "Science + En|Ph|Ch|Ma|Ec",
                    "fit_summary": "Good fit for analytical and logical strengths, but lower alignment with emotional and creative scores.",
                },
                {
                    "stream": "Humanities + En|Ec|Ps|Po|So",
                    "fit_summary": "Challenging fit, requiring development in areas like Psychology, less aligned with high business and strategic scores.",
                },
            ],
            "Conclusion": "Your final recommendations were chosen not just by subject popularity, but by how strongly each subject engages your top cognitive strengths (like 92 in Mechanical), emotional values (88 in Autonomy), and motivation (92 in Business + 88 in Persuasion). This personalized blend ensures both academic excellence and long-term career alignment.",
        },
    }

    prompt_all_pages_composite_report(user_id, "Composite", data)
