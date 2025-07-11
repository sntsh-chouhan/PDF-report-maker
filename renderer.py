import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import numpy as np
from matplotlib.lines import Line2D

def generate_pdf_for_user(user_id, page_data, page_number=None):
    env = Environment(loader=FileSystemLoader("templates"))
    template_name = page_data["template"]
    template = env.get_template(template_name)
    html_content = template.render(**page_data["context"])
    print(html_content)

    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    safe_template_name = template_name.replace('/', '_').replace('\\', '_').replace('.html', '')
    # Add page_number to filename if provided
    if page_number is not None:
        output_path = os.path.join(output_dir, f"{user_id}_{safe_template_name}_page{page_number}.pdf")
    else:
        output_path = os.path.join(output_dir, f"{user_id}_{safe_template_name}.pdf")

    HTML(string=html_content, base_url="static").write_pdf(output_path)
    print(f"PDF generated: {output_path}")
