# charts/radar_chart.py
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
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

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels, fontsize=9)
                        # Move labels outward
            # for label, angle in zip(self.get_xticklabels(), theta):
            #     label.set_horizontalalignment('center')

            #     # Calculate x and y offsets
            #     x = np.cos(angle)
            #     y = np.sin(angle)
            #     label.set_position((1.15 * x, 1.15 * y)) 

        def set_rscale_labels(self, ticks=None, angle=0):
            """
            Set radial scale (e.g., 20, 40, ..., 100).
            ticks: list of tick values (default = [20, 40, 60, 80, 100])
            angle: angle where labels appear (default = 90 degrees)
            """
            if ticks is None:
                ticks = [20, 40, 60, 80, 100]
            self.set_ylim(0, 100)
            self.set_rgrids(ticks, angle=angle, fontsize=20)

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
        


    register_projection(RadarAxes)
    return theta


def generate_radar_chart(user_id, factors):
    labels = list(factors.keys())
    values = list(factors.values())
    values += values[:1]  # close the loop

    theta = radar_factory(len(labels))  # gives len = 13
    theta = np.concatenate((theta, [theta[0]]))  # close the loop => len = 14

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
    # ax.set_rgrids([20, 40, 60, 80, 100])

    ax.plot(theta, values, color='#2F80ED', linewidth=2)
    ax.fill(theta, values, color='#2F80ED', alpha=0.3)
    ax.set_varlabels(labels)
    # fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))


    legend_circle = Line2D([], [], marker='o', color='w',
                           label='My Score - Interest Sub-factors',
                           markerfacecolor='#2F80ED', markersize=10, markeredgewidth=0)
    ax.legend(handles=[legend_circle],
              loc='lower center', bbox_to_anchor=(0.5, -0.2),
              fontsize=9, frameon=False)
    
    draw_radial_scale_labels(ax, ticks=[20, 40, 60, 80, 100], angle=90, radius_max=100)


    ax.spines['polar'].set_visible(False)
    ax.grid(True, color='gray', linestyle='dotted', linewidth=0.5)
    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.set_facecolor('white')

    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{user_id}.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    return f"charts/{user_id}.png"


def draw_radial_scale_labels(ax, ticks=[20, 40, 60, 80, 100], angle=180, radius_max=100, fontsize=10):
    """
    Manually draw radial scale labels at a given angle (default is top, i.e., 90°).
    """
    theta_rad = np.deg2rad(angle)
    for tick in ticks:
        radius = tick / radius_max  # Normalize if needed
        ax.text(
            theta_rad,
            tick,
            str(tick),
            ha='center',
            va='center',
            fontsize=fontsize,
            color='gray'
        )
