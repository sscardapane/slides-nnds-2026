
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import rcParams
import brewer2mpl

np.random.seed(1)

font_size = 9

matplotlib.use('Qt5Agg')

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

# Get a colors matrix
bmap = brewer2mpl.get_map('Set1', 'qualitative', 3)
colors = bmap.mpl_colors

np.random.seed(1)

x = np.arange(-10, 10, 0.01)
y = 1.0/(1.0+np.exp(-x))
     
y_derivative = y * (1 - y)

plt.figure()

plt.plot(x, y, color=colors[0])

plt.xlabel('$s$')
plt.ylabel('Sigmoid $\sigma(s)$')

plt.ylim((0-0.1, 1+0.1))

plt.grid(color="0.9", linestyle='--', linewidth=1)
plt.box(on=True)
plt.tight_layout()
plt.show(block=False)

plt.savefig('sigmoid.pdf', format='pdf',bbox_inches='tight', pad_inches=0)

plt.figure()

plt.plot(x, y, color=colors[0], label='$\sigma(s)$')
plt.plot(x, y_derivative, color=colors[1], label='$\sigma\'(s)$')
plt.xlabel('$s$')
plt.ylabel('Sigmoid and its derivative')

plt.ylim((0-0.1, 1+0.1))

plt.legend(loc=0)
plt.grid(color="0.9", linestyle='--', linewidth=1)
plt.box(on=True)
plt.tight_layout()
plt.show(block=False)

plt.savefig('sigmoid_and_derivative.pdf', format='pdf',bbox_inches='tight', pad_inches=0)
