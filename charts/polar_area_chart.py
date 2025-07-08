import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from matplotlib.projections.polar import PolarAxes
from matplotlib.lines import Line2D
from matplotlib.projections import register_projection



def generate_polar_area_chart(user_id, factor_name, data):
    # Prepare datalabels = list(data.keys())
    labels = list(data.keys())
    scores = [data[label]['user_score'] for label in labels]

    # Fixed 9-color palette
    colors = [
        "#85a4fe",
        "#918eec",
        "#9d76d6",
        "#a55ebc",
        "#ab429f",
        "#ab207f",
        "#ff98cc",
        "#ffab99",
        "#ffd072"
    ]

    N = len(scores)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    radii = scores
    width = 2 * np.pi / N

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.spines['polar'].set_visible(False)

    bars = ax.bar(theta, radii, width=width, bottom=0.0, color=colors, edgecolor='white')

    # Add labels
    for i, (bar, label) in enumerate(zip(bars, labels)):
        angle = theta[i]
        label_radius = 100 + 5  # 5 units outside the bar height

        x = label_radius * np.cos(angle)
        y = label_radius * np.sin(angle)

        ax.text(
            angle,
            label_radius,
            label,
            rotation=0,              # Keep all labels horizontal
            ha='center',
            va='center',
            fontsize=10,
            color='black'
        )

    ax.set_title(factor_name, fontsize=16, pad=20)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_xticks([])

    # Save chart
    chart_dir = os.path.join("static", "charts", factor_name.replace(" ", "_"))
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{user_id}_polar_area.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    return f"charts/{factor_name}/{user_id}_polar_area.png"