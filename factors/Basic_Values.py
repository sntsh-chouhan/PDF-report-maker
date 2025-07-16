import os
import json

from renderer import prompt_all_pages_independent_report
from gpt_helper import points_about_element_in_factor_report

def make_basic_value_component(user_id, user_detail, user_report):
    print("hello from Basic Values")
    with open("data/factor/Basic_Values.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = {}
    for i, key in enumerate(top_3_keys, start=1):
        gpt_data = points_about_element_in_factor_report(user_id, "Basic Values", key, user_report[key]["user_score"])

        if gpt_data is None:
            print("error at generating gpt data at user_id: ", user_id, "factor: Basic_Values and at element: ", key)

        top_3_interest[str(i)] = {
            "name": key,
            "score": user_report[key]["user_score"],
            "avg_score" : user_report[key]["global_avg"],
            "small_text": meta_data.get(key, {}).get("small_text", ""),
            "big_text": meta_data.get(key, {}).get("big_text", ""),
            "people_like_you": meta_data.get(key, {}).get("people_like_you", ""),
            "job_for_you": meta_data.get(key, {}).get("job_for_you", ""),
            "small_image": meta_data.get(key, {}).get("small_image", ""),
            "big_image": meta_data.get(key, {}).get("big_image", ""),
            "key_desc": gpt_data["element_para"],
            "key_point": gpt_data["meaning_for_you"]
        }
    
    # print(top_3_interest)

    first = top_3_interest["1"]
    second = top_3_interest["2"]
    third = top_3_interest["3"]
    

    data = {
        "page_1": {
            "index": "5",
            "model_part_1": "Purpose Alignment",
            "model_part_2": "Model (PAM)",
            "Factor": "Basic Values",
            "description" : """An evidence-based model to uncover core professional values
                    and guide long-term, purpose-driven career decisions.""",
            "background_image": "images/interests/front_page_basic_values.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7" : {
            "title" : "2. Results - Your Basic Values Profile",
            "paragraph" : """Your responses provide valuable insight into the core values that drive your decisions,
                    behaviors, and overall sense of fulfillment. The graph below highlights the values that
                    resonate most with you, offering a clear picture of what motivates you in both your personal
                    and professional life. These are not just abstract preferences; they represent the guiding
                    principles that shape how you define success, work with others, and navigate challenges.
                    Understanding your core values helps you identify the environments, roles, and relationships
                    that align with your true self. By recognizing these values, you’ll gain a deeper understanding
                    of what truly matters to you, allowing you to make more informed, purposeful decisions and
                    find greater satisfaction in both your career and personal endeavors.""",
            "type_of_graph" : "Baisc value Chart",
            "graph_image" : "charts/Basic_Values/common.png",
            "desc_graph" : """RStacked Bar Graph displaying your learning style across different dimensions. Each bar is split into
                    contrasting tendencies, showing your percentage alignment with each trait pair.""",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "7",
            "page_display" : "5",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Analysis - Your 3 Core (Basic) Values",
            "top_3_interest" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "graph_image" : "charts/Basic_Values/comperitive_bar.png",
            "desc_graph" : """Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the
                    group average. Subfactors under similar factors are grouped by color for easier comparison""",
            "Exhibit" : "Exhibit 4.1",
            "page_no." : "8",
            "page_display" : "6",
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
            "page_no." : "9",
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
            "page_no." : "10",
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
            "page_no." : "11",
            "page_display" : "9",
            "align":"",
            "user_detail" : user_detail
        }
    }

    prompt_all_pages_independent_report(user_id, "Basic Values", data)


