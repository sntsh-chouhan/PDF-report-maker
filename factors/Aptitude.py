import os
import json

from renderer import prompt_all_pages_independent_report
from gpt_helper import points_about_element_in_factor_report

def make_aptitude_component(user_id, user_detail, user_report):
    print("hello from aptitude")
    with open("data/factor/Aptitude.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = {}
    for i, key in enumerate(top_3_keys, start=1):
        gpt_data = points_about_element_in_factor_report(user_id, "Aptitude", key, user_report[key]["user_score"])

        if gpt_data is None:
            print("error at generating gpt data at user_id: ", user_id, "factor: Aptitude and at element: ", key)

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
            "index": "2",
            "model_part_1": "Auro Cognitive",
            "model_part_2": "Index (ACI)",
            "Factor": "Aptitude",
            "description" : """Go beyond IQ—explore the deeper cognitive abilities that define
                    how you learn, solve problems, and how you can minimize the
                    path between your initial endowment and your aspirations.""",
            "background_image": "images/cover/Aptitude.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7" : {
            "title" : "2. Results - Your Aptitude Profile",
            "paragraph" : """Your responses reveal your natural strengths and cognitive abilities across different areas of
                    aptitude. The graph below highlights the areas where you excel the most, providing insight into how
                    you approach problem-solving, learning, and adapting to new challenges. These are not just abilities;
                    they are strong indicators of where you are likely to perform best and achieve long-term success in
                    both academic and professional environments. By understanding your aptitudes, you’ll gain a clearer
                    understanding of your unique abilities, helping you make informed decisions about the paths where
                    you can thrive and excel.""",
            "type_of_graph" : "Aptitude Radial Graph",
            "graph_image" : "charts/Aptitude/common.png",
            "desc_graph" : """Radial displaying your aptitude scores across 9 factors, ranked by strength. Each sector represents a
                    factor, with higher values indicating stronger aptitudes.""",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "6",
            "page_display" : "4",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Analysis - Your Top 3 Aptitude Strengths",
            "top_3_interest" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "graph_image" : "charts/Aptitude/comperitive_bar.png",
            "desc_graph" : "Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the group average.",
            "Exhibit" : "Exhibit 4.1",
            "page_no." : "7",
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

    prompt_all_pages_independent_report(user_id, "Aptitude", data)


