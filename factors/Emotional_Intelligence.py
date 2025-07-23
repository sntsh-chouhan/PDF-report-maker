import os
import json

from renderer import prompt_all_pages_independent_report
from factors.helper import HelperFunction

def make_emotional_intelligence_component(user_id, user_detail, user_report):
    print("hello from Emotional Intelligence ")
    with open("data/factor/Emotional_Intelligence.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = HelperFunction.factor_helper(user_id, "Emotional Intelligence", top_3_keys, user_report, meta_data)
    
    # print(top_3_interest)

    first = top_3_interest["1"]
    second = top_3_interest["2"]
    third = top_3_interest["3"]
    

    data = {
        "page_1": {
            "index": "7",
            "model_part_1": "Auro EQ (AEQ)",
            "model_part_2": "",
            "Factor": "Emotional Intelligence",
            "description" : """Understand how your preferred way of working shapes your
                    effectiveness in academic and professional environments.""",
            "background_image": "images/cover/Emotional.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7" : {
            "title" : "2. Results - Your Emotional Intelligence Profile",
            "paragraph" : """Your responses reflect various aspects of emotional intelligence, highlighting how you
                    understand and manage emotions in yourself and others. The graph below emphasizes the
                    areas that most influence your ability to navigate social interactions, build relationships, and
                    lead effectively. These are not just traits, but key predictors of how you will handle
                    challenges, resolve conflicts, and stay motivated in both your personal and professional life.
                    By exploring these areas, you’ll gain valuable insights into your emotional strengths and
                    opportunities for growth, helping you to better understand yourself and enhance your
                    interactions with others.""",
            "type_of_graph" : "Spider Graph for Emotional Intelligence Report",
            "graph_image" : "charts/Emotional_Intelligence/common.png",
            "desc_graph" : """Spider graph displaying your interest scores across 6 factors, ranked by strength. Each axis
                    represents a factor, with higher values indicating stronger interests.""",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "6",
            "page_display" : "4",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Analysis - Your Top 3 EQ Strengths",
            "top_3_interest" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "graph_image" : "charts/Emotional_Intelligence/comperitive_bar.png",
            "desc_graph" : """Horizontal bar graph illustrating your scores relative to others, highlighting how you compare
                    to the group average.""",
            "Exhibit" : "Exhibit 4.1",
            "page_no." : "7",
            "page_display" : "5",
            "user_detail" : user_detail
        },
        "page_9" : {
            "title": "1st: " + first["name"],
            "name": first["name"],
            "big_text": first["big_text"],
            "big_image": first["big_image"],
            "people_like_you": first["people_like_you"],
            "job_for_you": first["job_for_you"],
            "score": first["score"],
            "avg_score": first["avg_score"],
            "profile_text": first["key_desc"],
            "profile_points": first["key_point"],
            "page_no." : "8",
            "page_display" : "7",
            "align":"",
            "user_detail" : user_detail
        },
        "page_10" : {
            "title": "2nd: " + second["name"],
            "name": second["name"],
            "big_text": second["big_text"],
            "big_image": second["big_image"],
            "people_like_you": second["people_like_you"],
            "job_for_you": second["job_for_you"],
            "score": second["score"],
            "avg_score": second["avg_score"],
            "profile_text": second["key_desc"],
            "profile_points": second["key_point"],
            "page_no." : "9",
            "page_display" : "8",
            "align":"reverse",
            "user_detail" : user_detail
        },
        "page_11" : {
            "title": "3rd: " + third["name"],
            "name": third["name"],
            "big_text": third["big_text"],
            "big_image": third["big_image"],
            "people_like_you": third["people_like_you"],
            "job_for_you": third["job_for_you"],
            "score": third["score"],
            "avg_score": third["avg_score"],
            "profile_text": third["key_desc"],
            "profile_points": third["key_point"],
            "page_no." : "10",
            "page_display" : "9",
            "align":"",
            "user_detail" : user_detail
        }
    }

    prompt_all_pages_independent_report(user_id, "Emotional Intelligence", data)

