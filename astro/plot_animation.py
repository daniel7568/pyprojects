import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

def update(frame):
    body1.set_xdata(x1_ls_f[:frame])
    body1.set_ydata(y1_ls_f[:frame])
    body2.set_xdata(x2_ls_f[:frame])
    body2.set_ydata(y2_ls_f[:frame])
    max_border = max(x1_ls_f[:frame+1] + y1_ls_f[:frame+1] + x2_ls_f[:frame+1] + y2_ls_f[:frame+1])*1.2
    min_border = min(x1_ls_f[:frame+1] + y1_ls_f[:frame+1] + x2_ls_f[:frame+1] + y2_ls_f[:frame+1])*1.2
    ax.set_xlim(left=min_border,right=max_border)
    ax.set_ylim(bottom=min_border,top=max_border)
    return body1,body2

with open("path_data.csv", newline='') as f:
   reader = csv.reader(f, delimiter=' ')
   raw_data = list(reader)
   raw_data.pop(0)
   x1_ls = [float(ls[0]) for ls in raw_data]
   y1_ls = [float(ls[1]) for ls in raw_data]
   x2_ls = [float(ls[2]) for ls in raw_data]
   y2_ls = [float(ls[3]) for ls in raw_data]

skip = 100

x1_ls_f = []
y1_ls_f = []
x2_ls_f = []
y2_ls_f = []
for step in range(len(x1_ls)):
    if step % skip == 0:
        x1_ls_f.append(x1_ls[step])
        y1_ls_f.append(y1_ls[step])
        x2_ls_f.append(x2_ls[step])
        y2_ls_f.append(y2_ls[step])

fig, ax = plt.subplots()

body1 = ax.plot(x1_ls_f[0],y1_ls_f[0],marker='.')[0]
body2 = ax.plot(x2_ls_f[0],y2_ls_f[0],marker='.')[0]

ani = animation.FuncAnimation(fig=fig,func = update,frames = len(x1_ls_f), interval=0.0001,blit = True)

plt.show()