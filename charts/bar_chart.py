import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def generate_bar_chart(user_id, factor, input_data):
    """Generates a clean horizontal bar chart and returns the relative path to the saved image."""

    factors = {key: value["user_score"] for key, value in input_data.items()}

    labels = list(factors.keys())
    values = list(factors.values())

    fig, ax = plt.subplots(figsize=(7.5, 5))
    bars = ax.barh(labels, values, color='#2F80ED')

    # Add value labels at the end of each bar
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 2, bar.get_y() + bar.get_height() / 2, f"{w:.0f}", va='center', fontsize=8)

    # Axis limits and labels
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    # ax.set_xlabel("Score", fontsize=9)
    # ax.set_ylabel("Sub-Factor", fontsize=9)

    # Remove axis spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Remove tick marks (small dashes)
    ax.tick_params(axis='y', which='both', length=0)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    # Legend
    circle_marker = Line2D(
        [], [], marker='o', color='w', label='My Score',
        markerfacecolor='#2F80ED', markersize=10, markeredgewidth=0
    )
    ax.legend(
        handles=[circle_marker],
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        fontsize=8,
        frameon=False
    )

    # Styling
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # Save chart
    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{factor}/{user_id}_bar.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{factor}/{user_id}_bar.png"
