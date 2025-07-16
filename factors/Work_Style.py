import os
import json

from renderer import prompt_all_pages_independent_report
from gpt_helper import points_about_element_in_factor_report

def make_work_style_component(user_id, user_detail, user_report):
    print("hello from work style")
    with open("data/factor/Work_Style.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = {}
    for i, key in enumerate(top_3_keys, start=1):
        gpt_data = points_about_element_in_factor_report(user_id, "Work Style", key, user_report[key]["user_score"])

        if gpt_data is None:
            print("error at generating gpt data at user_id: ", user_id, "factor: Work_Style and at element: ", key)

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
            "index": "6",
            "model_part_1": "Auro Productivity",
            "model_part_2": "Optimizer (APO)",
            "Factor": "Work Style",
            "description" : """Understand how your preferred way of working shapes your
                    effectiveness in academic and professional environments.""",
            "background_image": "images/interests/front_page_basic_values.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7" : {
            "title" : "2. Results - Your Work Style Profile",
            "paragraph" : """Your responses offer a comprehensive understanding of how you approach tasks, collaborate with
                    others, and adapt to different work environments. The graph below highlights the areas of your
                    work style where you excel, revealing how you prefer to structure your tasks, work independently,
                    and interact with others. These are not just preferences; they are key factors that influence your
                    comfort and performance in various professional settings. Whether you thrive in structured
                    environments or excel with autonomy, understanding your work style helps you align with roles and
                    teams that support your strengths. By recognizing how you work best, you’ll gain valuable insights
                    into the environments that bring out your full potential, allowing you to achieve greater satisfaction
                    and success in your career.""",
            "type_of_graph" : "Star Graph for Work Style Report",
            "graph_image" : "charts/Work_Style/common.png",
            "desc_graph" : """Star graph displaying your work style scores across various factors, with each point on the star
                    representing a specific trait. The longer the radius, the stronger your preference in that area.""",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "8",
            "page_display" : "5",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Analysis - Your Top 3 Work Style",
            "top_3_interest" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "graph_image" : "charts/Work_Style/comperitive_bar.png",
            "desc_graph" : """Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the
                    group average. Subfactors under similar factors are grouped by color for easier comparison.""",
            "Exhibit" : "Exhibit 4.1",
            "page_no." : "9",
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
            "page_no." : "10",
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
            "page_no." : "11",
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
            "page_no." : "12",
            "page_display" : "9",
            "align":"",
            "user_detail" : user_detail
        }
    }

    prompt_all_pages_independent_report(user_id, "Work_Style", data)


