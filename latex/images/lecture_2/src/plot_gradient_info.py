
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

x = np.arange(-4, 10, 0.01)
y = x**2 - 1.5*x

dy = 2*x - 1.5

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(x, y, color=colors[1])
plt.plot((-2, 4), (7, 10), 'o', color=colors[0])

ax.annotate(r'$\displaystyle\partial f(x) < 0$', xy=(-2, 7), xytext=(0, 30),
    arrowprops=dict(facecolor='gray', width=1, headwidth=8, headlength=5, shrink=0.15),
)

y_tan = -5.5 * (x + 2.0) + 7
plt.plot(x, y_tan, '--r', alpha=0.4)

ax.annotate(r'$\displaystyle\partial f(x) > 0$', xy=(4, 10), xytext=(6, -2),
    arrowprops=dict(facecolor='gray', width=1, headwidth=8, headlength=5, shrink=0.15),
)

y_tan = 6.5 * (x - 4.0) + 10
plt.plot(x, y_tan, '--r', alpha=0.4)

plt.xlim([-4, 10])
plt.ylim([-15, 85])

plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')

plt.grid(color="0.9", linestyle='--', linewidth=1)
plt.box(on=True)
plt.tight_layout()
plt.show(block=False)

plt.savefig('gradient_info.pdf', format='pdf',bbox_inches='tight', pad_inches=0)