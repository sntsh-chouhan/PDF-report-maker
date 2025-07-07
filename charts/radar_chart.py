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


def radar_factory(num_vars, frame='circle'):
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):
        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars, radius=.5, edgecolor="k")
            raise ValueError(f"Unknown frame: {frame}")

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(
                    axes=self, spine_type='circle',
                    path=Path.unit_regular_polygon(num_vars)
                )
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5) + self.transAxes)
                return {'polar': spine}
            raise ValueError(f"Unknown frame: {frame}")

        # def set_varlabels(self, labels, values):
        #     # Calculate ranks
        #     ranks = sorted([(v, i) for i, v in enumerate(values)], reverse=True)
        #     rank_map = {i: f"({rank + 1})" for rank, (_, i) in enumerate(ranks)}
        #     labeled = [f"{label} {rank_map[i]}" for i, label in enumerate(labels)]

        #     self.set_xticklabels([])  # remove default labels

        #     # Draw custom tick labels with last 3 characters in blue
        #     for i, (label, angle) in enumerate(zip(labeled, theta[:-1])):
        #         angle_deg = np.degrees(angle) % 360
        #         label_text = label[:-4]
        #         rank_text = label[-4:]

        #         # Alignment rules
        #         if angle_deg == 0 or angle_deg == 180:
        #             ha = 'center'
        #         elif 0 < angle_deg < 180:
        #             ha = 'right'
        #         else:
        #             ha = 'left'

        #         # Auto radius calculation
        #         max_radius = self.get_ylim()[1]
        #         label_radius = max_radius * 1.08

        #         self.text(
        #             angle, label_radius+2, label_text,
        #             ha=ha, va='center',
        #             fontsize=12, fontweight='medium',
        #             color='black'
        #         )
        #         self.text(
        #             angle, label_radius, rank_text,
        #             ha=ha, va='center',
        #             fontsize=12, fontweight='medium',
        #             color='#2F80ED'
        #         )


                # final_text = main_text + blue_text
                


        def set_varlabels(self, labels, values):
            # Calculate ranks
            ranks = sorted([(v, i) for i, v in enumerate(values)], reverse=True)
            rank_map = {i: f"({rank + 1})" for rank, (_, i) in enumerate(ranks)}
            labeled = [f"{label} {rank_map[i]}" for i, label in enumerate(labels)]
            self.set_thetagrids(
                np.degrees(theta),
                labeled,
                fontsize=12,
                fontweight='medium',
                color='black'
            )
            for i, label in enumerate(self.get_xticklabels()):
                label.set_color('black')

        def draw_radial_scale_labels(self, ticks=[20, 40, 60, 80, 100], angle=270, radius_max=100):
            theta_rad = 0
            for tick in ticks:
                radius = tick / radius_max
                self.text(
                    theta_rad,
                    tick,
                    str(tick),
                    ha='center',
                    va='center',
                    fontsize=15,
                    color='black',
                    fontweight='medium'
                )

    register_projection(RadarAxes)
    return theta


def generate_radar_chart(user_id, factor, input_data):

    factors = {key: value["user_score"] for key, value in input_data.items()}

    labels = list(factors.keys())
    values = list(factors.values())
    values += values[:1]  # close the loop

    theta = radar_factory(len(labels))
    theta = np.concatenate((theta, [theta[0]]))  # close the loop

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))

    ax.plot(theta, values, color='#2F80ED', linewidth=2)
    ax.fill(theta, values, color='#2F80ED', alpha=0.3)
    ax.set_varlabels(labels, values[:-1])

    legend_circle = Line2D([], [], marker='o', color='w',
                           label='My Score - Interest Sub-factors',
                           markerfacecolor='#2F80ED', markersize=10, markeredgewidth=0)
    ax.legend(
        handles=[legend_circle],
        loc='lower center',
        bbox_to_anchor=(0.5, -0.2),
        fontsize=12, frameon=False
    )

    ax.draw_radial_scale_labels(ticks=[20, 40, 60, 80, 100], angle=90, radius_max=100)

    ax.spines['polar'].set_visible(False)
    ax.grid(True, color='gray', linestyle='dashed', linewidth=0.5)
    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.set_facecolor('white')

    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{factor}/{user_id}_radial.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{factor}/{user_id}_radial.png"

