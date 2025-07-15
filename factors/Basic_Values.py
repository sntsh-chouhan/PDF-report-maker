import os
import json

from renderer import prompt_all_pages_independent_report

def make_basic_value_component(user_id, user_detail, user_report):
    print("hello from career")
    with open("data/factor/career_interest.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(user_report, key=lambda k: user_report[k]['user_score'], reverse=True)[:3]
    
    top_3_interest = {}
    for i, key in enumerate(top_3_keys, start=1):
        top_3_interest[str(i)] = {
            "name": key,
            "score": user_report[key]["user_score"],
            "avg_score" : user_report[key]["global_avg"],
            "small_text": meta_data.get(key, {}).get("small_text", ""),
            "big_text": meta_data.get(key, {}).get("big_text", ""),
            "people_like_you": meta_data.get(key, {}).get("people_like_you", ""),
            "small_image": meta_data.get(key, {}).get("small_image", ""),
            "big_image": meta_data.get(key, {}).get("big_image", "")
        }
    
    # print(top_3_interest)

    first = top_3_interest["1"]
    second = top_3_interest["2"]
    third = top_3_interest["3"]
    

    data = {
        "page_1" :{
            "index" : "1",
            "model" : "Ariston Interest Alignment (AIA)",
            "Factor" : "Career Interest",
            "background_image" : "path to image",
            "user_detail" : user_detail
        },
        "page_7" : {
            "title" : "2. Results - Your Interest Profile",
            "paragraph" : "Your responses reflect varying levels of motivation across different areas of work and life. The graph below highlights the domains that excite and engage you the most, offering a clear picture of where your true interests lie. These are not just preferences; they are strong indicators of long-term satisfaction, growth, and performance in both your academic journey and professional career. By understanding these patterns, you’ll gain deeper insights into yourself, empowering you to make more informed choices as you pursue your goals and ambitions.",
            "type_of_graph" : "Interest Spider Graph",
            "desc_graph" : "Spider graph displaying your interest scores across 11 factors, ranked by strength. Each axis represents a factor, with higher values indicating stronger interests.",
            "Exhibit" : "Exhibit 2.1",
            "page_no." : "7",
            "user_detail" : user_detail
        },
        "page_8" : {
            "title_1" : "3. Your Top 3 Interests",
            "top_3_interst" : top_3_interest,

            "title_2" : "4. How you compare to others",
            "desc_graph" : "Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the group average.",
            "Exhibit" : "Exhibit 2.2",
            "page_no." : "8",
            "user_detail" : user_detail
        },
        "page_9" : {
            "title": "1st: " + first["name"],
            "name": first["name"],
            "big_text": first["big_text"],
            "big_image": first["big_image"],
            "people_like_you": first["people_like_you"],
            "score": first["score"],
            "avg_score": first["avg_score"],
            "page_no." : "7",
            "user_detail" : user_detail
        },
        "page_10" : {
            "title": "1st: " + second["name"],
            "name": second["name"],
            "big_text": second["big_text"],
            "big_image": second["big_image"],
            "people_like_you": second["people_like_you"],
            "score": second["score"],
            "avg_score": second["avg_score"],
            "page_no." : "7",
            "user_detail" : user_detail
        },
        "page_11" : {
            "title": "1st: " + third["name"],
            "name": third["name"],
            "big_text": third["big_text"],
            "big_image": third["big_image"],
            "people_like_you": third["people_like_you"],
            "score": third["score"],
            "avg_score": third["avg_score"],
            "page_no." : "7",
            "user_detail" : user_detail
        }
    }

    prompt_all_pages_independent_report(user_id, "Basic_Values", data)


