import os
import json

from renderer import generate_pdf_for_user


def make_career_component(user_id, user_detail, user_report):
    print("hello from career")
    with open("data/factor/career_interest.json") as f:
        meta_data = json.load(f)

    top_3_keys = sorted(
        user_report, key=lambda k: user_report[k]["user_score"], reverse=True
    )[:3]

    top_3_interest = {}
    for i, key in enumerate(top_3_keys, start=1):
        top_3_interest[str(i)] = {
            "name": key,
            "score": user_report[key]["user_score"],
            "avg_score": user_report[key]["global_avg"],
            "small_text": meta_data.get(key, {}).get("small_text", ""),
            "big_text": meta_data.get(key, {}).get("big_text", ""),
            "people_like_you": meta_data.get(key, {}).get("people_like_you", ""),
            "small_image": meta_data.get(key, {}).get("small_image", ""),
            "big_image": meta_data.get(key, {}).get("big_image", ""),
        }

    print(top_3_interest)

    first = top_3_interest["1"]
    second = top_3_interest["2"]
    third = top_3_interest["3"]

    data = {
        "page_1": {
            "index": "1",
            "model": "Ariston Interest Alignment (AIA)",
            "Factor": "Career Interest",
            "description" : """An evidence-based model to uncover core professionl values 
and guide long-term, purpose-driven career
sions.""",
            "background_image": "images/interests/front_page_basic_values.png",
            "factors": ["Interest", "Aptitude", "Personality", "Learning Styles", "Basic Values", "Work Style", "Emotional Intelligence"], # pass all factors in array only 
            "user_detail": user_detail,
        },
        "page_7": {
            "title": "2. Results - Your Interest Profile",
            "paragraph": "Your responses reflect varying levels of motivation across different areas of work and life. The graph below highlights the domains that excite and engage you the most, offering a clear picture of where your true interests lie. These are not just preferences; they are strong indicators of long-term satisfaction, growth, and performance in both your academic journey and professional career. By understanding these patterns, you’ll gain deeper insights into yourself, empowering you to make more informed choices as you pursue your goals and ambitions.",
            "type_of_graph": "Interest Spider Graph",
            "chart_path": "charts/Career_Interest/111_radial_bar.png",
            "desc_graph": "Spider graph displaying your interest scores across 11 factors, ranked by strength. Each axis represents a factor, with higher values indicating stronger interests.",
            "Exhibit": "Exhibit 2.1",
            "page_no": "5",
            "user_detail": user_detail,
        },
        "page_8": {
            "title_1": "3. Your Top 3 Interests",
            "top_3_interest": top_3_interest,
            "chart_path": "charts/Career_Interest/111_comperitive_bar.png",
            "title_2": "4. How you compare to others",
            "desc_graph": "Horizontal bar graph illustrating your scores relative to others, highlighting how you compare to the group average.",
            "Exhibit": "Exhibit 2.2",
            "page_no": "6",
            "user_detail": user_detail,
        },
        "page_9": {
            "title": "1st: " + first["name"],
            "name": first["name"],
            "big_text": first["big_text"],
            "big_image": "images/interests/interest_large_1.png",
            "people_like_you": first["people_like_you"],
            "score": first["score"],
            "profile_text": """You have a natural drive for entrepreneurship, leadership, and
strategic thinking. You are energized by goals, targets,
opportunities, and the challenge of building something impactful.
This suggests that you're not just interested in making decisions
—you want those decisions to move things forward, create
value, and bring measurable outcomes. Whether it's running
your own venture or driving growth within a company, you thrive
in environments that are competitive, fast-paced, and outcome-
focused. You'll likely feel at home in roles related to business
development, marketing strategy, finance, operations
management, or startup leadership.""",
            "profile_points": [
                "You enjoy planning and taking the initiative.",
                "You seek performance-driven roles where success is visible and rewarded.",
                "You are comfortable taking calculated risks.",
            ],
            "career_profile": [
                "Entrepreneuer",
                "Buisness Consultant",
                "Financial Analyst",
            ],
            "avg_score": first["avg_score"],
            "user_detail": user_detail,
            "align":"",
            "page_no": 7,
        },
        "page_10": {
            "title": "1st: " + second["name"],
            "name": second["name"],
            "big_text": second["big_text"],
            "big_image": "images/interests/interest_large_2.png",
            "people_like_you": second["people_like_you"],
            "score": second["score"],
            "avg_score": second["avg_score"],
            "user_detail": user_detail,
            "profile_text": """You have a natural drive for entrepreneurship, leadership, and
strategic thinking. You are energized by goals, targets,
opportunities, and the challenge of building something impactful.
This suggests that you're not just interested in making decisions
—you want those decisions to move things forward, create
value, and bring measurable outcomes. Whether it's running
your own venture or driving growth within a company, you thrive
in environments that are competitive, fast-paced, and outcome-
focused. You'll likely feel at home in roles related to business
development, marketing strategy, finance, operations
management, or startup leadership.""",
            "profile_points": [
                "You enjoy planning and taking the initiative.",
                "You seek performance-driven roles where success is visible and rewarded.",
                "You are comfortable taking calculated risks.",
            ],
            "career_profile": [
                "Entrepreneuer",
                "Buisness Consultant",
                "Financial Analyst",
            ],
            "align":"reverse",
            "page_no": 8,
        },
        "page_11": {
            "title": "1st: " + third["name"],
            "name": third["name"],
            "big_text": third["big_text"],
            "big_image": "images/interests/interest_large_3.png",
            "people_like_you": third["people_like_you"],
            "score": third["score"],
            "avg_score": third["avg_score"],
            "user_detail": user_detail,
            "profile_text": """You have a natural drive for entrepreneurship, leadership, and
strategic thinking. You are energized by goals, targets,
opportunities, and the challenge of building something impactful.
This suggests that you're not just interested in making decisions
—you want those decisions to move things forward, create
value, and bring measurable outcomes. Whether it's running
your own venture or driving growth within a company, you thrive
in environments that are competitive, fast-paced, and outcome-
focused. You'll likely feel at home in roles related to business
development, marketing strategy, finance, operations
management, or startup leadership.""",
            "profile_points": [
                "You enjoy planning and taking the initiative.",
                "You seek performance-driven roles where success is visible and rewarded.",
                "You are comfortable taking calculated risks.",
            ],
            "career_profile": [
                "Entrepreneuer",
                "Buisness Consultant",
                "Financial Analyst",
            ],
            "align":"",
            "page_no": 9,
        },
    }
    page_data = {}

    # make front page
    # page_data["template"] = "pages/front_page.html"
    # page_data["context"] = data["page_1"]
    # generate_pdf_for_user(user_id, page_data)

    # make page 7
    # data["page_7"]["report_title"] = "Career Interest"  # or any title you want

    # page_data["template"] = "pages/page_wth_element_chart.html"
    # page_data["context"] = data["page_7"]
    # generate_pdf_for_user(user_id, page_data)

    # make page_8
    page_data["template"] = "pages/page_with_top_3_elements.html"
    page_data["context"] = data["page_8"]
    generate_pdf_for_user(user_id, page_data)

    # make page_9
    # page_data["template"] = "pages/page_with_interests.html"
    # page_data["context"] = data["page_9"]
    # generate_pdf_for_user(user_id, page_data, page_number=9)

    # make page_10
    # page_data["template"] = "pages/page_with_interests.html"
    # page_data["context"] = data["page_10"]
    # generate_pdf_for_user(user_id, page_data, page_number=10)

    # make page_11
    # page_data["template"] = "pages/page_with_interests.html"
    # page_data["context"] = data["page_11"]
    # generate_pdf_for_user(user_id, page_data, page_number=11)

    print(json.dumps(page_data, indent=4))


# make_front_page(1, "Ariston Interest Alignment (AIA)", "Career Interest", user_detail)

# make_front_page()
