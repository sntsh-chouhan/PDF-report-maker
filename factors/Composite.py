import os
import json

from renderer import prompt_all_pages_independent_report
from gpt_helper import streat_overview
from gpt_helper import stream_recomendation_depth_explanation
from gpt_helper import stream_intrest_alinment_explanation
from factors.helper import HelperFunction

def make_composite_component(user_id, user_detail, user_report):
    print("hello from composite")
    with open("data/factor/Aptitude.json") as f:
        meta_data = json.load(f)

    factor_list = [
        "Career_Interest", "Aptitude", "Personality",
        "Learning_Style", "Basic_Values", "Work_Style",
        "Emotional_Intelligence"
    ]
    common_report = HelperFunction.build_report(factor_list, "common", 2)
    comperitive_bar_report = HelperFunction.build_report(factor_list, "comperitive_bar", 3)


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

    stream_reccomendation = HelperFunction.stream_reccomendation_function(user_report["streams"], user_report["subjects"])
    stream_overview_text = streat_overview(user_id, stream_reccomendation)

    cleaned_factor_data = HelperFunction.clean_factor_data(user_report["factors"])

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
            "data" : common_report,
            "page_no." : "4",
            "page_display" : "3"

        },
        "page_5" : {
            "data" : common_report_summary,
            "page_no." : "5",
            "page_display" : "6"
        },
        "page_6" : {
            "title" : "2. Summary Report",
            "paragraph" : """You are very strong in Business, Mechanical
                    Reasoning, Assertiveness, Visual Learning,
                    Autonomy, Unpredictability, and Self-
                    Regulation. These factors dominated the
                    results of your 7 diagnostic tests.""",
            "note" : """*Note: The average, minimum, and maximum scores are
                    computed based on global student data for this test.""",
            "data" : comperitive_bar_report,
            "page_no." : "6",
            "page_display" : "7",
        },
        "page_7" : {
            "data" : common_report_summary,
            "page_no." : "7",
            "page_display" : "8",
        },
        "page_8" : {
            "data" : stream_reccomendation,
            "points" : stream_overview_text,
            "page_no." : "7",
            "page_display" : "8",
        },
        "page_9" : {
            "stream" : stream_reccomendation["1"]["stream"],
            "title" : "5. Subject and Stream Recommendation Analysis",
            "sub_title" : f"Stream Recommendation 1 & 2 : {stream_reccomendation['1']['stream']}",
            "meta_data" : [
                stream_reccomendation["1"],
                stream_reccomendation["2"]
            ],
            "data" : stream_recomendation_depth_explanation(user_id, {"1" : stream_reccomendation["1"] , "2" : stream_reccomendation["2"]}, cleaned_factor_data, "Best Suit"),
            "page_no." : "7",
            "page_display" : "8",
        },
        "page_10" : {
            "data" : stream_intrest_alinment_explanation(user_id, {"1" : stream_reccomendation["1"] , "2" : stream_reccomendation["2"]}, cleaned_factor_data["Career Interest"])
        },
        "page_11":{
            "stream" : stream_reccomendation["3"]["stream"],
            "title" : "5. Subject and Stream Recommendation Analysis",
            "sub_title" : f"Stream Recommendation 3 : {stream_reccomendation['3']['stream']}",
            "meta_data" : [
                stream_reccomendation["3"]
            ],
            "data" : stream_recomendation_depth_explanation(user_id, {"3" : stream_reccomendation["3"]}, cleaned_factor_data, "Can try"),
            "page_no." : "7",
            "page_display" : "8",
        },
        "page_12" : {
            "data" : stream_intrest_alinment_explanation(user_id, {"3" : stream_reccomendation["3"]}, cleaned_factor_data["Career Interest"])
        },
        "page_13":{
            "stream" : stream_reccomendation["4"]["stream"],
            "title" : "5. Subject and Stream Recommendation Analysis",
            "sub_title" : f"Stream Recommendation 3 : {stream_reccomendation['4']['stream']}",
            "meta_data" : [
                stream_reccomendation["4"]
            ],
            "data" : stream_recomendation_depth_explanation(user_id, {"4" : stream_reccomendation["4"]}, cleaned_factor_data, "Should Ignore"),
            "page_no." : "7",
            "page_display" : "8",
        },
        "page_14" : {
            "data" : stream_intrest_alinment_explanation(user_id, {"4" : stream_reccomendation["4"]}, cleaned_factor_data["Career Interest"])
        }

    
    }

    # print(json.dumps(data["page_9"], indent= 2))
    print(json.dumps(data["page_10"], indent= 2))
    # prompt_all_pages_independent_report(user_id, "Compo", data)
