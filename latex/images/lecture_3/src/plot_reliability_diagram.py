import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from pylab import rcParams

np.random.seed(1)

font_size = 9

# Set parameters for plotting
params = {
   'axes.labelsize': font_size,
   'axes.linewidth': 1,
   'font.size': font_size,
   'legend.fontsize': font_size-2,
   'xtick.labelsize': font_size,
   'xtick.major.size': 2,
   'ytick.labelsize': font_size,
   'ytick.major.size': 2,
   'text.usetex': True,
   'figure.figsize': [4*0.9,3*0.9],
}
rcParams.update(params)

colors = ['#DAE8FC', '#EA6B66', '#6C8EBF', '#666666']

np.random.seed(1)

x_axis = np.linspace(0, 1, 10)
acc = [0., 0.05, 0.1, 0.25, 0.48, 0.58, 0.75, 0.9, 0.98, 1.]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_axisbelow(True)
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

plt.plot(x_axis, x_axis, '--', color=colors[3], label='Perfect calibration')

plt.bar(x_axis, acc, width=0.08, facecolor=colors[0], edgecolor='black', linewidth=1.5)

for i in range(len(x_axis)):
    ax.fill_between(np.linspace(x_axis[i] - 0.04, x_axis[i] + 0.04, 10),
                    acc[i] if acc[i] < x_axis[i] else x_axis[i],
                    x_axis[i] if acc[i] < x_axis[i] else acc[i],
                    color=colors[1], edgecolor='black', linewidth=1.5, zorder=10,
                    label='Miscalibration' if i==0 else None)

plt.xlabel('Confidence')
plt.ylabel('Accuracy')

leg = plt.legend(loc='upper left')
fr = leg.get_frame()
fr.set_lw(0.5)
fr.set_facecolor('none')

plt.grid(alpha=0.35, linewidth=1, zorder=0)
plt.box(on=True)
plt.tight_layout()
output_path = Path(__file__).resolve().parents[1] / 'reliability_plot.pdf'
plt.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.01,
            transparent=True)
