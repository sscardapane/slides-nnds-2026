
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

f = lambda x: x**2 - 1.5*x
df = lambda x: 2*x - 1.5

x = 0.5
f_linearized = lambda h: f(x) + df(x)*(h - x)

print(f(x + 0.01))
print(f_linearized(x + 0.01))

xrange = np.linspace(-1, 1, 100)

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(xrange, f(xrange), color=colors[1], label='f(x)')
plt.plot(xrange, f_linearized(xrange), color=colors[0], label='Linearized at 0.5')

ax.fill_between(xrange, f(xrange), f_linearized(xrange), facecolor='gray', alpha=0.1, interpolate=True)

plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')

plt.legend()
plt.grid(color="0.9", linestyle='--', linewidth=1)
plt.box(on=True)
plt.tight_layout()
plt.show()

plt.savefig('taylor_approximation.pdf', format='pdf',bbox_inches='tight', pad_inches=0)