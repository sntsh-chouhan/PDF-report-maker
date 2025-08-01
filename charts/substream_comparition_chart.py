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

def get_annotation_data(data, subjects):
    top_data = HelperFunction.stream_reccomendation_function(data, subjects)

    annotations_data = {
        "1": {
            "target_label": f"{top_data['1']['stream']} ({top_data['1']['subject_mapping']})",
            "color": "#3539e0"
        },
        "2": {
            "target_label": f"{top_data['2']['stream']} ({top_data['2']['subject_mapping']})",
            "color": "#7947eb"
        },
        "3": {
            "target_label": f"{top_data['3']['stream']} ({top_data['3']['subject_mapping']})",
            "color": "#b51eda"
        },
        "4": {
            "target_label": f"{top_data['4']['stream']} ({top_data['4']['subject_mapping']})",
            "color": "#bc231c"
        }
    }
    return annotations_data

# --- FUNCTION TO ADD CIRCLES ---
def add_annotations(ax, annotations_data, all_labels, all_scores):
    """
    Draws numbered, circular-looking annotations with custom colors.
    """
    for circle_num, data in annotations_data.items():
        target_label = data.get("target_label")
        # Get the custom color, or fall back to a default gray if not provided
        color = data.get("color", "#4A4A4A") 

        if not target_label:
            continue

        try:
            bar_index = all_labels.index(target_label)
        except ValueError:
            print(f"Warning: Label '{target_label}' not found. Skipping annotation '{circle_num}'.")
            continue

        bar_score = all_scores[bar_index]
        y_pos = bar_index
        circle_x_pos = bar_score / 2

        # Use an Ellipse to create a visually circular shape
        ellipse = mpatches.Ellipse(
            (circle_x_pos, y_pos),
            width=2.2,
            height=1,
            facecolor='white',
            edgecolor=color,  # Use the custom color for the border
            linewidth=2,
            zorder=5
        )
        ax.add_patch(ellipse)

        # Draw the number text inside the circle
        ax.text(
            circle_x_pos,
            y_pos,
            str(circle_num),
            ha='center',
            va='center',
            fontsize=13,
            fontweight='bold',
            color=color,  # Use the custom color for the text
            zorder=6
        )

def generate_stream_comparison_chart(user_id, data, subjects, factor="Stream_Comparison") -> str:
    print("making composite graph")
    """
    Generates a horizontal stream comparison chart with all legends organized below the graph.
    """

    labels, scores, bar_colors = prepare_stream_data(data)
    y_pos = np.arange(len(labels))

    annotations_data = get_annotation_data(data, subjects)

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

    if annotations_data:
        add_annotations(ax, annotations_data, labels, scores)

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

    # -- Row 2: Acronyms --# -- Row 2: Acronyms --
    legend_ax.text(0.5, 0.75, "Acronyms:", fontsize=13, fontweight='bold', ha='center', va='top')

    acronym_mapping = HelperFunction.subject_acronyms()
    acronym_mapping = {v: k for k, v in acronym_mapping.items()}
    sorted_items = sorted(acronym_mapping.items())

    # Calculate the size of each of the four columns
    n_items = len(sorted_items)
    col_size = (n_items + 3) // 4  # Calculates ceiling(n/4)

    # Split the list into four parts
    col1_items = sorted_items[0 : col_size]
    col2_items = sorted_items[col_size : 2 * col_size]
    col3_items = sorted_items[2 * col_size : 3 * col_size]
    col4_items = sorted_items[3 * col_size :]

    # Create the text string for each column
    col1_text = "\n".join([f"{k:<4} {v}" for k, v in col1_items])
    col2_text = "\n".join([f"{k:<4} {v}" for k, v in col2_items])
    col3_text = "\n".join([f"{k:<4} {v}" for k, v in col3_items])
    col4_text = "\n".join([f"{k:<4} {v}" for k, v in col4_items])

    # Position the four columns of text horizontally
    legend_ax.text(-0.08, 0.65, col1_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)
    legend_ax.text(0.18, 0.65, col2_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)
    legend_ax.text(0.545, 0.65, col3_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)
    legend_ax.text(0.85, 0.65, col4_text, fontsize=11, va='top', ha='left', family='monospace', linespacing=1.6)

    # -- Row 3: Note --
    # legend_ax.text(0.01, 0.05, "Note:", fontsize=13, fontweight='bold', ha='left', va='top')
    note = "Darker hues indicate higher compatibility scores, while lighter hues signify lower scores."
    legend_ax.text(0.1, 0.2, note, fontsize=11, ha='left', va='top', style='italic', wrap=True)

    # 4. FINALIZE AND SAVE
    fig.subplots_adjust(
        left=0.15, 
        right=0.85, 
        top=0.999, 
        bottom=-0.01, 
        hspace=0.1  # Re-including hspace from the first call
    )
    
    chart_dir = os.path.join("static", "charts", factor.replace(" ", "_"))
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, "stream.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()

    return f"charts/{factor}/stream.png"