import os
import json

from renderer import prompt_all_pages_independent_report
from factors.helper import HelperFunction

def make_learning_style_component(user_id, user_detail, user_report):
    print("hello from learning style")
    with open("data/factor/Learning_style.json") as f:
        meta_data = json.load(f)
        
    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = HelperFunction.factor_helper(user_id, "Learning Style", top_3_keys, user_report, meta_data)
    
    
    # print(top_3_interest)

    first = top_3_interest["1"]
    second = top_3_interest["2"]
    third = top_3_interest["3"]
    

    data = {
        "page_1": {
            "index": "4",
            "model_part_1": "Auro Learn",
            "model_part_2": "Matrix (ALM)",
            "Factor": "Learning Style",
            "description" : """Adaptive learning strategies tailored to your cognitive style—for more
                    efficient, effective, and enjoyable learning.""",
            "background_image": "images/cover/Learning.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7" : {
            "title" : "2. Results - Your Learning Style Profile",
            "paragraph" : """Your responses reveal how you naturally approach learning, from how you absorb and
                    process information to how you manage your time and study habits. The graph below
                    highlights your dominant learning preferences, giving you insight into the methods and
                    environments that best support your growth and retention. These are not just preferences—
                    they are powerful indicators of how you’ll excel in different academic and professional
                    settings. Understanding your unique learning style allows you to tailor your approach to suit
                    your strengths, helping you navigate challenges with greater ease and confidence. By
                    recognizing these patterns, you’ll gain deeper self-awareness, empowering you to adopt
                    strategies that make learning more effective, enjoyable, and sustainable, both in school and
                    throughout your career.""",
            "type_of_graph" : "Learning Style Chart",
            "graph_image" : "charts/Learning_Style/common.png",
            "desc_graph" : """Stacked Bar Graph displaying your learning style across different dimensions. Each bar is split into
                    contrasting tendencies, showing your percentage alignment with each trait pair.""",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "9",
            "page_display" : "6",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Analysis - Your Top 3 Learning Strengths",
            "top_3_interest" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "graph_image" : "charts/Learning_Style/comperitive_bar.png",
            "desc_graph" : """Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the
                    group average. Subfactors under similar factors are grouped by color for easier comparison""",
            "Exhibit" : "Exhibit 4.1",
            "page_no." : "10",
            "page_display" : "7",
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
            "page_no." : "11",
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
            "page_no." : "12",
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
            "page_no." : "13",
            "page_display" : "9",
            "align":"",
            "user_detail" : user_detail
        }
    }

    prompt_all_pages_independent_report(user_id, "Learning Style", data)


