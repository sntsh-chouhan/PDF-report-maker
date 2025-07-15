import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import numpy as np
from matplotlib.lines import Line2D

def prompt_all_pages_independent_report(user_id, factor, data):
    page_data = {}

    # make front page 
    page_data["template"] = "front_page.html"
    page_data["context"] = data["page_1"]
    generate_pdf_for_user(user_id, factor, page_data)

    # # make page 7
    # page_data["template"] = "page_wth_element_chart.html"
    # page_data["context"] = data["page_7"]
    # generate_pdf_for_user(user_id, factor, page_data)

    # # make page_8
    # page_data["template"] = "page_with_top_3_elements.html"
    # page_data["context"] = data["page_8"]
    # generate_pdf_for_user(user_id, factor, page_data)
    
    # # make page_9
    # page_data["template"] = "page_with_elements_left.html"
    # page_data["context"] = data["page_9"]
    # generate_pdf_for_user(user_id, factor, page_data)
    
    # # make page_10
    # page_data["template"] = "page_with_elements_right.html"
    # page_data["context"] = data["page_10"]
    # generate_pdf_for_user(user_id, factor, page_data)
    
    # # make page_11
    # page_data["template"] = "page_with_elements_left.html"
    # page_data["context"] = data["page_11"]
    # generate_pdf_for_user(user_id, factor, page_data)


def generate_pdf_for_user(user_id, factor, page_data):

    env = Environment(loader=FileSystemLoader("templates/pages"))

    # Load template dynamically
    template_name = page_data["template"]
    template = env.get_template(template_name)

    # Render HTML using context dictionary
    html_content = template.render(**page_data["context"])
    # Save PDF
    output_dir = f"reports/{user_id}/{factor}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{user_id}_{template_name.replace('.html', '')}.pdf")

    HTML(string=html_content, base_url=os.path.abspath("static")).write_pdf(output_path)
    
    print(f"PDF generated: {output_path}")
