
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import brewer2mpl

font_size = 18

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
   'figure.figsize': [4*1.5,3*1.5],
}
rcParams.update(params)

# Get a colors matrix
bmap = brewer2mpl.get_map('Set1', 'qualitative', 3)
colors = bmap.mpl_colors

np.random.seed(1)

x = np.arange(-10, 10, 0.01)
y = x**3

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(x, y, color=colors[1])
plt.plot((0), (0), 'o', color=colors[0], markersize=8)

ax.annotate('Saddle point \n (neither minimum \n nor maximum)', xy=(0, 0), xytext=(2, -700),
    arrowprops=dict(facecolor='gray', width=1, headwidth=8, headlength=5, shrink=0.15),
)

#plt.xlim([1, 8])

plt.xlabel(r'$\theta$')
plt.ylabel(r'$J(\theta)$')

ax.get_xaxis().set_ticklabels([])
ax.get_yaxis().set_ticklabels([])

plt.grid(color="0.9", linestyle='--', linewidth=1)
plt.box(on=True)
plt.tight_layout()
plt.show()

plt.savefig('saddle_point.pdf', format='pdf',bbox_inches='tight', pad_inches=0)