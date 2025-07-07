import os
import matplotlib.pyplot as plt

def generate_subfactor_bar_chart(user_id, factor, subfactor_data: dict):
    """
    Generates a horizontal bar chart with legend horizontally aligned on top,
    sorted by user_score in descending order.
    """

    # Step 1: Sort subfactor data by user_score (descending)
    sorted_items = sorted(subfactor_data.items(), key=lambda item: item[1]["user_score"], reverse=True)
    
    # Step 2: Unpack the sorted values
    subfactors = [k for k, _ in sorted_items][::-1]  # reverse for better top-down layout
    user_scores = [v["user_score"] for _, v in sorted_items][::-1]
    avg_scores = [v["global_avg"] for _, v in sorted_items][::-1]
    min_scores = [v["global_min"] for _, v in sorted_items][::-1]
    max_scores = [v["global_max"] for _, v in sorted_items][::-1]

    # Setup figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw bars and markers
    bars = ax.barh(subfactors, user_scores, color='#85A4FE', label='Your Score')
    ax.scatter(min_scores, subfactors, color="#E8E400", marker='^', label='Min')
    ax.scatter(max_scores, subfactors, color='#F75C03', marker='o', label='Max')
    ax.scatter(avg_scores, subfactors, color='#5F54A0', marker='s', label='Average')

    # Labels on bars
    for bar in bars:
        xval = bar.get_width()
        ax.text(xval + 1, bar.get_y() + bar.get_height() / 2, f"{xval:.0f}", 
                va='center', ha='left', fontsize=9)

    # Styling
    ax.set_xlim(0, 110)
    ax.set_xlabel("Scores", fontsize=12)
    ax.set_ylabel("Subfactors", fontsize=12)
    ax.set_title("Subfactor Comparison: You vs Global", fontsize=14, pad=30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Move legend to top, horizontal
    ax.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, 1.02),
        ncol=4,
        fontsize=9,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave space at top for legend

    # Save chart
    chart_dir = os.path.join("static", "charts")    
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{factor}/{user_id}_global_comparision_bar.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{factor}/{user_id}_global_comparision_bar.png"
