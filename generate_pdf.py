import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import numpy as np
from matplotlib.lines import Line2D
from charts.radar_chart import generate_radar_chart
from charts.bar_chart import generate_bar_chart
from charts.dual_bar_chart import generate_dual_bar_chart
from charts.comparitive_bar_chart import generate_subfactor_bar_chart
from charts.polar_area_chart import generate_polar_area_chart


from factors.career_interest import make_career_component

def generate_pdf_for_user(user_id: str):
    """Main driver to render PDF for a single user."""
    # Load user info
    with open("data/students.json") as f:
        students = json.load(f)

    user = next((u for u in students if u["id"] == user_id), None)
    if not user:
        print(f"User {user_id} not found in students.json")
        return

    # Load factor data
    with open("data/factor_data.json") as f:
        factor_data_all = json.load(f)

    factor_entry = factor_data_all.get(str(user_id))
    if not factor_entry or not factor_entry.get("data"):
        print(f"No factor data found for user {user_id}")
        return

    factors = factor_entry["data"]["factors"]
    description = factor_entry["data"].get("description", "")

    # Generate chart
    # chart_path = generate_radar_chart(user_id, factors)
    # chart_path = generate_bar_chart(user_id, factors)
    chart_path = generate_dual_bar_chart(user_id, "stuff", factors)
    # chart_path = generate_subfactor_bar_chart(user_id, "stuff", factors)
    # chart_path = generate_polar_area_chart(user_id, "stuff", factors)
    

    # generate_subfactor_bar_chart
    
    # Setup template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("page_2.html")
    # template = env.get_template("front_page.html")

    html_content = template.render(
        student=user,
        chart_path=chart_path,
        factors=factors,
        description=description,
        report_title="Personality Report"
    )

    # Save PDF
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{user_id}_page_2.pdf")

    HTML(string=html_content, base_url="static").write_pdf(output_path)
    print(f"PDF generated: {output_path}")



def start_makeing_all_charts(user_id):
    with open("data/new_data_diagnostic.json") as f:
        all_data = json.load(f)["data"]

    # Loop through each factor
    for factor, traits in all_data["factors"].items():
        print("factor:", factor)
        # print("traits:", traits)

        if factor == "Career Interest":
            generate_radar_chart(user_id, factor, traits)
        if factor == "Aptitude":
            generate_polar_area_chart(user_id, factor, traits)
        if factor == "Personality":
            generate_dual_bar_chart(user_id, factor, traits)
        if factor == "Learning Style":
            generate_dual_bar_chart(user_id, factor, traits)
        if factor == "Basic Values":
            generate_dual_bar_chart(user_id, factor, traits)
        if factor == "Work Style":
            generate_radar_chart(user_id, factor, traits)
        if factor == "Emotional Intelligence":
            generate_radar_chart(user_id, factor, traits)

        generate_subfactor_bar_chart(user_id, factor, traits)
        
        print("done")

def make_all_pdf():
    user_id = 2611

    # user_detail = get_user_detail(user_id)
    # user_report = get_user_report(user_id)
    user_detail ={
        "name" : "Santosh Chouhan",
        "Class" : "9",
        "year" : "June 2025" 
    }
    with open("data/new_data_diagnostic.json") as f:
        all_data = json.load(f)["data"]

    # start_makeing_all_charts(user_id)

    # 7 iteration of same code to get componnet of the pdf

    # career interest
    make_career_component(user_id, user_detail, all_data["factors"]["Career Interest"])
    # make_front_page(1, "Ariston Interest Alignment (AIA)", "Career Interest", user_detail)
    # aptitude
    # personality
    # learning style
    # basic values
    # work style
    # emotinal inteligence



if __name__ == "__main__":
    # start_makeing_all_charts("111")
    make_all_pdf()
    # generate_pdf_for_user("101")  # Replace "101" with the target user ID
