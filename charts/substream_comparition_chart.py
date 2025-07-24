import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgb
from factors.helper import HelperFunction
import json


def get_stream_group(label: str) -> str:
    if "Science" in label:
        return "Science"
    elif "Humanities" in label:
        return "Humanities"
    else:
        return "Commerce"
    
def hex_to_rgb_tuple(hex_color):
    """Convert hex to normalized RGB tuple."""
    return np.array(to_rgb(hex_color))


def interpolate_color(start_color, end_color, ratio):
    """Linearly interpolate between two RGB colors."""
    return start_color + (end_color - start_color) * ratio


def apply_gradient_colors(labels, scores):
    """Assign gradient-based colors for each stream."""
    if not scores:
        return []
        
    max_score = max(scores)
    min_score = min(scores)
    score_range = max_score - min_score
    
    if score_range == 0:
        score_range = 1

    gradient_ranges = {
        "Science": {
            "min": hex_to_rgb_tuple("#C0FF82"),
            "max": hex_to_rgb_tuple("#7CFC00"),
        },
        "Humanities": {
            "min": hex_to_rgb_tuple("#7ACAFF"),
            "max": hex_to_rgb_tuple("#0099FF"),
        },
        "Commerce": {
            "min": hex_to_rgb_tuple("#FFEB91"),
            "max": hex_to_rgb_tuple("#FFD000"),
        },
    }

    colors = []
    for label, score in zip(labels, scores):
        ratio = (score - min_score) / score_range
        stream_type = get_stream_group(label)
        start_color = gradient_ranges[stream_type]["min"]
        end_color = gradient_ranges[stream_type]["max"]
        interpolated_rgb = interpolate_color(start_color, end_color, ratio)
        colors.append(interpolated_rgb)

    return colors

def prepare_stream_data(data):
    """Prepare labels and scores dynamically from data."""
    label_score_pairs = []

    for stream_name, substreams in data.items():
        for recommendation in substreams:
            subject_code = HelperFunction.get_subject_mapped(recommendation["subjects"])
            label = f"{stream_name} ({subject_code})"
            score = recommendation["average_score"]
            label_score_pairs.append((label, score))

    sorted_pairs = sorted(label_score_pairs, key=lambda x: x[1], reverse=True)
    
    if not sorted_pairs:
        return [], [], []
        
    sorted_labels, sorted_scores = zip(*sorted_pairs)
    colors = apply_gradient_colors(sorted_labels, sorted_scores)

    return sorted_labels, sorted_scores, colors


def generate_stream_comparison_chart(user_id, data, factor="Stream_Comparison") -> str:
    """
    Generates a horizontal stream comparison chart with all legends organized below the graph.
    """

    labels, scores, bar_colors = prepare_stream_data(data)
    y_pos = np.arange(len(labels))

    # 1. SETUP FIGURE AND AXES
    # Create a figure with two subplots stacked vertically (2 rows, 1 column).
    # `height_ratios` makes the top chart area taller than the bottom legend area.
    fig, (ax, legend_ax) = plt.subplots(
        2, 1,
        figsize=(12, 16), # Taller figure to accommodate legends below
        gridspec_kw={'height_ratios': [3, 1]}
    )
    # fig.suptitle("Stream Compatibility Analysis", fontsize=18, fontweight='bold')

    # 2. PLOT THE MAIN CHART (TOP PANEL)
    bars = ax.barh(y_pos, scores, color=bar_colors, height=0.8)

    for i, (score, label) in enumerate(zip(scores, labels)):
        subject_codes = label.split('(')[-1].replace(')', '')
        ax.text(score + 1.0, i, f"{round(score)}% : ({subject_codes})", va='center', fontsize=11)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{label.split(' ')[0]} . {i+1}" for i, label in enumerate(labels)], fontsize=12)
    ax.set_xlabel("Score", fontsize=14, labelpad=10)
    ax.invert_yaxis()
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    ax.set_facecolor('white')
    ax.tick_params(axis='x', which='major', labelsize=12)
    ax.set_xlim(right=(max(scores) + 5) if scores else 105) # Dynamic padding for text

    for spine in ax.spines.values():
        spine.set_visible(False)

    # 3. POPULATE THE LEGEND PANEL (BOTTOM PANEL)
    legend_ax.axis("off") # Hide the axis frame

    # -- Row 1: Stream Color Legend --
    # legend_ax.text(0.01, 0.9, "Stream Color Key:", fontsize=13, fontweight='bold', ha='left', va='top')
    legend_patches = [
        mpatches.Patch(color="#7CFC00", label="Science"),
        mpatches.Patch(color="#0099FF", label="Humanities"),
        mpatches.Patch(color="#FFD000", label="Commerce")
    ]
    legend_ax.legend(
        handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 0.95),
        ncol=3, frameon=False, fontsize=12
    )

    # -- Row 2: Acronyms --
    legend_ax.text(0.5, 0.75, "Acronyms:", fontsize=13, fontweight='bold', ha='center', va='top')
    acronym_mapping = {
        "E": "English", "P": "Physics", "C": "Chemistry", "B": "Biology",
        "En": "Economics", "M": "Mathematics", "Pe": "Physical Education",
        "Cs": "Computer Science", "Hs": "Home Science", "I": "Informatics Practices",
        "Py": "Psychology", "So": "Sociology", "G": "Geography", "L": "Legal Studies",
        "Mu": "Music", "F": "Fine Arts"
    }
    sorted_items = sorted(acronym_mapping.items())
    mid_point = (len(sorted_items) + 1) // 2
    col1_text = "\n".join([f"{k:<4} {v}" for k, v in sorted_items[:mid_point]])
    col2_text = "\n".join([f"{k:<4} {v}" for k, v in sorted_items[mid_point:]])
    
    legend_ax.text(0.2, 0.65, col1_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)
    legend_ax.text(0.5, 0.65, col2_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)

    # -- Row 3: Note --
    # legend_ax.text(0.01, 0.05, "Note:", fontsize=13, fontweight='bold', ha='left', va='top')
    note = "Darker hues indicate higher compatibility scores, while lighter hues signify lower scores."
    legend_ax.text(0.1, 0.05, note, fontsize=11, ha='left', va='top', style='italic', wrap=True)

    # 4. FINALIZE AND SAVE
    fig.subplots_adjust(
        left=0.15, 
        right=0.85, 
        top=0.999, 
        bottom=0.025, 
        hspace=0.1  # Re-including hspace from the first call
    )
    
    chart_dir = os.path.join("static", "charts", factor.replace(" ", "_"))
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, "stream.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()

    return f"charts/{factor}/stream.png"