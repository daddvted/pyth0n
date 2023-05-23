import matplotlib.pyplot as plt
from math import pi

# Abilities data
ted_abilities = {
    'COMPUTER': 62,
    'ENGLISH': 55,
    'LONGBOARD': 40,
    'UKULELE': 35,
    'DRIVING': 50,
}

# number of variable
# categories=list(df)[1:]
categories = ted_abilities.keys()
N = len(categories)

# But we need to repeat the first value to close the circular graph:
values=list(ted_abilities.values())
values += values[:1]

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories, color='#0047BD', size=10)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0,20,40,60,80], ["0","20","40","60","80"], color="#000000", size=8)
plt.ylim(0,100)

# Plot data
ax.plot(angles, values, linewidth=1.5, linestyle='solid', color='#009543')

# Fill area
ax.fill(angles, values, 'b', color='#00AB38', alpha=0.6)

plt.show()
