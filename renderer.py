import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import numpy as np
from matplotlib.lines import Line2D

def prompt_all_pages_composite_report(user_id, comp, data):
    page_data = {}

    # # graph summary 
    # page_data["template"] = "composite/graph_summary.html"
    # page_data["context"] = data["page_4"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=1)
    
    # # # summary text 
    # page_data["template"] = "composite/summary_text.html"
    # page_data["context"] = data["page_5"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=2)
    
    # # # graph summary 
    # page_data["template"] = "composite/graph_summary.html"
    # page_data["context"] = data["page_6"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=3)
    
    # # # summary text 
    # page_data["template"] = "composite/summary_text.html"
    # page_data["context"] = data["page_7"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=4)
    
    # # subject and stream recommendation analysis
    # page_data["template"] = "composite/stream_recommendation.html"
    # page_data["context"] = data["page_8"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=5)
    
    # # subject and stream recommendation analysis
    # page_data["template"] = "composite/stream_recommendation_analysis.html"
    # page_data["context"] = data["page_9"]
    # generate_pdf_for_user(user_id, comp, page_data, page_number=6)
    
    # Interest Alignment Page
    page_data["template"] = "composite/interest_alignment.html"
    page_data["context"] = data["page_10"]
    generate_pdf_for_user(user_id, comp, page_data, page_number=7)
    
def prompt_all_pages_independent_report(user_id, factor, data):
    page_data = {}

    # make front page 
    page_data["template"] = "front_page.html"
    page_data["context"] = data["page_1"]
    generate_pdf_for_user(user_id, factor, page_data, page_number=1)

    # make page 7
    page_data["template"] = "page_wth_element_chart.html"
    page_data["context"] = data["page_7"]
    generate_pdf_for_user(user_id, factor, page_data, data["page_7"]["page_no."])

    # make page_8
    page_data["template"] = "page_with_top_3_elements.html"
    page_data["context"] = data["page_8"]
    generate_pdf_for_user(user_id, factor, page_data, data["page_8"]["page_no."])
    
    # make page_9
    page_data["template"] = "page_with_interests1.html"
    page_data["context"] = data["page_9"]
    generate_pdf_for_user(user_id, factor, page_data, data["page_9"]["page_no."])
    
    # # make page_10
    page_data["template"] = "page_with_interests2.html"
    page_data["context"] = data["page_10"]
    generate_pdf_for_user(user_id, factor, page_data, data["page_10"]["page_no."])

    # make page_11
    page_data["template"] = "page_with_interests3.html"
    page_data["context"] = data["page_11"]
    generate_pdf_for_user(user_id, factor, page_data, data["page_11"]["page_no."])


def generate_pdf_for_user(user_id, factor, page_data, page_number = None):

    env = Environment(loader=FileSystemLoader("templates/pages"))

    # Load template dynamically
    template_name = page_data["template"]
    template = env.get_template(template_name)

    # page meta data
    page_data["context"]["factor"] = factor
    html_content = template.render(**page_data["context"])

    # make factor safe for file naming
    factor = factor.replace(" ", "_")

    # Save PDF
    output_dir = f"reports/users/{user_id}/{factor}"
    os.makedirs(output_dir, exist_ok=True)

    # this is fail switch which will never happen unless you do some stupid shit
    safe_template_name = template_name.replace('/', '_').replace('\\', '_').replace('.html', '')
    
    # Add page_number to filename if provided
    if page_number is not None:
        output_path = os.path.join(output_dir, f"{page_number}.pdf")
    else:
        output_path = os.path.join(output_dir, f"{user_id}_{safe_template_name}.pdf")

    HTML(string=html_content, base_url=os.path.abspath("static")).write_pdf(output_path)
    
    print(f"PDF generated: {output_path}")

    
    # --- Always write HTML to output.html for preview ---
    # with open("output.html", "w", encoding="utf-8") as f:
    #     f.write(html_content)
    # print("HTML preview written to output.html")