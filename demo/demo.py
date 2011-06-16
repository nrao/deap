import matplotlib
import matplotlib.cm as cm
from pylab import arange, meshgrid, normpdf, exp, randn, sin, pi, cos, array

def func3(x,y):
    return (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)

f = get_figure()
f.subplots_adjust(wspace = 0.5, hspace = 0.9)

# Subplot 1
s1 = f.add_subplot(331)
t = arange(0.0, 2.0, 0.01)
s = sin(2*pi*t)
c = cos(2*pi*t)
p = s1.plot(t, s, linewidth=1.0)
p = s1.plot(t, c, linewidth=1.0)
p = s1.set_xlabel('time (s)')
p = s1.set_ylabel('voltage (mV)')
t1 = s1.set_title('Simple plot')
s1.grid(True)

# Subplot 2
s2 = f.add_subplot(332)
t = arange(0.0, 1.01, 0.01)
s = sin(2*2*pi*t)
p = s2.fill(t, s*exp(-5*t), 'r')
s2.grid(True)
p = s2.set_title('Filled area')

# Subplot 3
dx, dy = 0.025, 0.025
x = arange(-3.0, 3.0, dx)
y = arange(-3.0, 3.0, dy)
X,Y = meshgrid(x, y)
Z = func3(X, Y)
s3 = f.add_subplot(333)
p = s3.imshow(Z, cmap=cm.jet, extent=(-3, 3, -3, 3))
t3 = s3.set_title("Image")

# Subplot 4
dx, dy = 0.05, 0.05
x = arange(-3.0, 3.0, dx)
y = arange(-3.0, 3.0, dy)
X,Y = meshgrid(x, y)
xmin, xmax, ymin, ymax = min(x), max(x), min(y), max(y)
extent = xmin, xmax, ymin, ymax
Z1 = array(([0,1]*4 + [1,0]*4)*4); Z1.shape = 8,8  # chessboard
Z2 = func3(X, Y)
s4 = f.add_subplot(334)
p = s4.imshow(Z1, cmap=cm.gray, interpolation='nearest', extent=extent)
s4.hold(True)
p = s4.imshow(Z2, cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
t4 = s4.set_title("Layered Images")

# Subplot 5
mu, sigma = 100, 15
x = mu + sigma*randn(10000)
s5 = f.add_subplot(335)
n, bins, patches = s5.hist(x, 100, normed=1)
y = normpdf(bins, mu, sigma)
l = s5.plot(bins, y, 'r--', linewidth=2)
p = s5.set_xlim((40, 160))
t = s5.set_xlabel('Smarts')
t = s5.set_ylabel('P')
t5 = s5.set_title('Histogram')

# Subplot 6
s6 = f.add_subplot(336)
p = s6.contour(Z2)
t6 = s6.set_title("Contour")

# Subplot 7
r = arange(0,1,0.001)
theta = 2*2*pi*r
matplotlib.rc('grid', color='#316931', linewidth=1, linestyle='-')
matplotlib.rc('tick', labelsize=12)
s7 = f.add_subplot(3, 3, 7, polar=True, axisbg='#d5de9c')
p = s7.plot(theta, r, color='#ee8d18', lw=3)
#pylab.set(s7.thetagridlabels, y=1.075) # the radius of the grid labels
t7 = s7.set_title("Polar")
matplotlib.rcdefaults()

# Subplot 8
s8 = f.add_subplot(338)
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
fracs = [15, 30, 45, 10]
explode = [0, 0.05, 0, 0]
p = s8.pie(fracs, explode = explode, labels = labels, autopct = "%1.1f%%", shadow = True)
t8 = s8.set_title("Pie Anyone?")

# Subplot 9
dt = 0.01
t = arange(dt, 20.0, dt)
s9 = f.add_subplot(339)
p = s9.loglog(t, 20*exp(-t/10.0), basey=4)
s9.xaxis.grid(True, which='minor')  # minor grid on too
t = s9.set_xlabel('time (s)')
t = s9.set_ylabel('loglog')
s9.grid(True)
t9 = s9.set_title("Log-Log")
