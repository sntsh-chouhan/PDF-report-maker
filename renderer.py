import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import numpy as np
from matplotlib.lines import Line2D

def generate_pdf_for_user(user_id, page_data):

    env = Environment(loader=FileSystemLoader("templates/pages"))

    # Load template dynamically
    template_name = page_data["template"]
    template = env.get_template(template_name)

    # Render HTML using context dictionary
    html_content = template.render(**page_data["context"])
    print(html_content) 
    # Save PDF
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{user_id}_{template_name.replace('.html', '')}.pdf")

    HTML(string=html_content, base_url="static").write_pdf(output_path)
    
    print(f"PDF generated: {output_path}")
