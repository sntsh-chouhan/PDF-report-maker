import os
import matplotlib.pyplot as plt
from collections import defaultdict

def generate_subfactor_bar_chart(user_id, factor, subfactor_data: dict):
    """
    Generates a horizontal grouped bar chart by subfactor category with distinct colors,
    sorted by user_score descending.
    """

    # Define a color palette for different groups (rotate if >8 groups)
    color_palette = [
        "#85a4fe",  # sof-blue
        "#918eec",  # light violet
        "#9d76d6",  # orchid
        "#a55ebc",  # purple
        "#ab429f",  # magenta
        "#ab207f",  # deep rose
        "#ff98cc",  # pink
        "#cee9ff",  # pastel blue
        "#fcd4ff"   # soft lavender-pink (replaces duplicate)
    ]

    # Step 1: Sort by user_score
    sorted_items = sorted(subfactor_data.items(), key=lambda item: item[1]["user_score"], reverse=True)

    # Step 2: Group color assignment
    label_to_group = {}
    group_colors = {}
    current_color_idx = 0

    def extract_group(label):
        if " (" in label:
            return label.split(" (")[0].strip()
        elif "-" in label:
            return label.split("-")[0].strip()
        else:
            return label.split()[0].strip()

    for label, _ in sorted_items:
        group = extract_group(label)
        label_to_group[label] = group
        if group not in group_colors:
            group_colors[group] = color_palette[current_color_idx % len(color_palette)]
            current_color_idx += 1

    # Step 3: Unpack for plotting (reversed for top-down view)
    subfactors = [k for k, _ in sorted_items][::-1]
    user_scores = [v["user_score"] for _, v in sorted_items][::-1]
    avg_scores = [v["global_avg"] for _, v in sorted_items][::-1]
    min_scores = [v["global_min"] for _, v in sorted_items][::-1]
    max_scores = [v["global_max"] for _, v in sorted_items][::-1]
    bar_colors = [group_colors[label_to_group[k]] for k in subfactors]

    # Step 4: Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.barh(subfactors, user_scores, color=bar_colors, label='Your Score')
    ax.scatter(min_scores, subfactors, color="#E8E400", marker='^', label='Min')
    ax.scatter(max_scores, subfactors, color='#F75C03', marker='o', label='Max')
    ax.scatter(avg_scores, subfactors, color='#5F54A0', marker='s', label='Average')

    for bar in bars:
        xval = bar.get_width()
        ax.text(xval + 1, bar.get_y() + bar.get_height() / 2, f"{xval:.0f}",
                va='center', ha='left', fontsize=9)

    ax.set_xlim(0, 110)
    ax.set_xlabel("Scores", fontsize=12)
    ax.set_ylabel("Subfactors", fontsize=12)
    ax.set_title("Subfactor Comparison: You vs Global", fontsize=14, pad=30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    ax.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, 1.02),
        ncol=4,
        fontsize=9,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    chart_dir = os.path.join("static", "charts", factor.replace(" ", "_"))
    os.makedirs(chart_dir, exist_ok=True)

    chart_path = os.path.join(chart_dir, f"comperitive_bar.png")
    
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{factor}/comperitive_bar.png"
