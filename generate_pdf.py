import os
import json
from pypdf import PdfReader, PdfWriter
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
from charts.substream_comparition_chart import generate_stream_comparison_chart

from factors.Composite import make_composite_component
from factors.Career_interest import make_career_component
from factors.Aptitude import make_aptitude_component
from factors.Personality import make_personality_component
from factors.Learning_style import make_learning_style_component
from factors.Basic_Values import make_basic_value_component
from factors.Work_Style import make_work_style_component
from factors.Emotional_Intelligence import make_emotional_intelligence_component
from factors.Composite import make_composite_component

def stich_all_report(folder1, folder2, output_path="merged_output.pdf"):
    writer = PdfWriter()
    current_num = 1

    while current_num <= 100:
        filename = f"{current_num}.pdf"
        path1 = os.path.join(folder1, filename)
        path2 = os.path.join(folder2, filename)

        if os.path.exists(path1):
            reader = PdfReader(path1)
        elif os.path.exists(path2):
            reader = PdfReader(path2)
        else:
            print(f"Missing {current_num}.pdf in both folders. Stopping.")
            break  # Stop if neither folder has the file

        # Add pages if file was found
        for page in reader.pages:
            writer.add_page(page)

        current_num += 1

    if writer.pages:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"Merged PDF saved to {output_path}")
        return output_path
    else:
        print("No PDFs found. Nothing to merge.")
        return None

def start_makeing_all_charts(user_id, all_data):
    # Loop through each factor
    for factor, traits in all_data["factors"].items():
        print("making charts for factor:", factor)
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

    generate_stream_comparison_chart(user_id, all_data["streams"], all_data["subjects"]) 

def make_all_pdf(user_id, user_detail, all_data):
    # 7 iteration of same code to get componnet of the pdf

    # career interest
    make_career_component(user_id, user_detail, all_data["factors"]["Career Interest"])
    # aptitude
    make_aptitude_component(user_id, user_detail, all_data["factors"]["Aptitude"])
    # personality
    make_personality_component(user_id, user_detail, all_data["factors"]["Personality"])
    # learning style
    make_learning_style_component(user_id, user_detail, all_data["factors"]["Learning Style"])
    # basic values
    make_basic_value_component(user_id, user_detail, all_data["factors"]["Basic Values"])
    # work style
    make_work_style_component(user_id, user_detail, all_data["factors"]["Work Style"])
    # emotinal inteligence
    make_emotional_intelligence_component(user_id, user_detail, all_data["factors"]["Emotional Intelligence"])
    # Composite
    make_composite_component(user_id, user_detail, all_data)

    factor_list = [
        "Career_Interest", "Aptitude", "Personality",
        "Learning_Style", "Basic_Values", "Work_Style",
        "Emotional_Intelligence", "Composite"
    ]
    
    # factor_list = ["Composite"]
    
    for factor in factor_list:

        folder1=f"reports/static/{factor}"
        folder2=f"reports/users/{user_id}/{factor}"
        output_path=f"reports/users/{user_id}/merged/{factor}.pdf"
        stich_all_report(folder1, folder2, output_path)

if __name__ == "__main__":
    user_id = 11111

    # user_detail = get_user_detail(user_id)
    # user_report = get_user_report(user_id)
    user_detail ={
        "user_id" : user_id,
        "name" : "Dummy User",
        "Class" : "10",
        "year" : "June 2025" 
    }

    # with open("data/factor_data.json") as f:
    #     all_data = json.load(f)["data"]

    with open("data/new_data_diagnostic.json") as f:
        all_data = json.load(f)["data"]


    start_makeing_all_charts(user_id, all_data)
    # print("Made all the charts")
    make_all_pdf(user_id, user_detail, all_data)

    print(f"\033[92m All Done for user: {user_id}\033[0m")
