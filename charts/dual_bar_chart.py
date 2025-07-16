import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def generate_dual_bar_chart(user_id, factor_prime, trait_data):
    """
    Generates a dual horizontal bar chart sorted in descending order by left trait value (blue),
    showing left and right trait scores with colored bars and labels.
    """

    user_scores = {key: value["user_score"] for key, value in trait_data.items()}


    # Step 1: Group data into {factor: {left_label: val, right_label: val}}
    grouped = {}
    for label, value in user_scores.items():
        if "(" in label and label.endswith(")"):
            factor = label.split(" (")[0].strip()
            trait = label.split(" (")[1].rstrip(")").strip()
            if factor not in grouped:
                grouped[factor] = {}
            grouped[factor][trait] = value
        else:
            grouped[label] = {"": value}

    # Step 2: Convert to sortable list
    sortable = []
    for factor, traits in grouped.items():
        keys = list(traits.keys())
        values = list(traits.values())
        left_label = keys[0] if len(keys) > 0 else ""
        left_val = values[0] if len(values) > 0 else 0
        right_label = keys[1] if len(keys) > 1 else ""
        right_val = values[1] if len(values) > 1 else 0
        sortable.append((factor, left_label, left_val, right_label, right_val))

    # Step 3: Sort by left_val descending
    sortable.sort(key=lambda x: x[2], reverse=False)

    # Step 4: Plotting
    fig, ax = plt.subplots(figsize=(8, len(sortable) * 1.1))
    height = 0.35
    left_color = "#2853F5"
    right_color = "#BF21E7"

    for i, (factor, left_label, left_val, right_label, right_val) in enumerate(sortable):
        # Left bar (blue)
        ax.barh(i, left_val, height, color=left_color)

        # Right bar (violet)
        ax.barh(i, right_val, height, left=left_val, color=right_color)

        # Yellow marker at end of left bar
        ax.add_patch(Rectangle((left_val - 0.5, i - height / 2), 0.5, height, color='gold'))

        # Trait labels
        if left_val >right_val:
            left_weight = 'bold'
            right_weight = 'normal'
        elif left_val == right_val:
            left_weight = 'bold'
            right_weight = 'bold'            
        else:
            left_weight = 'normal'
            right_weight = 'bold'

        # Trait labels
        if left_label:
            ax.text(0, i - 0.35, f"{left_val:.0f}% {left_label}",
                    ha='left', va='center', fontsize=10,
                    fontweight=left_weight, color='dimgray')
        if right_label:
            ax.text(100, i - 0.35, f"{right_val:.0f}% {right_label}",
                    ha='right', va='center', fontsize=10,
                    fontweight=right_weight, color='dimgray')

        # Factor label
        ax.text(-5, i, factor, ha='right', va='center', fontsize=10, fontweight='bold')

    # Step 5: Cleanup
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, len(sortable))
    ax.axis('off')
    plt.tight_layout()

    # Step 6: Save chart
    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)   
    factor_prime = factor_prime.replace(" ", "_")
    chart_path = os.path.join(chart_dir, f"{factor_prime}/common.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{factor_prime}/common.png"
