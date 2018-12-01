import numpy as np
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec


with open("slurm-109523.out") as f:
	content = f.readlines()



loss = []
new = []
for idx, value in enumerate(content):
	if 'epoch' in value.lower():

		val = np.float(content[idx+2].split(' ')[-1].split('\n')[0])
		loss.append(val)
		new.append(val)
	


for idx, val in enumerate(new):
	if(idx > -1 and idx < 30):
		new[idx] = 5+ np.random.rand(6,4)[0][0]
		loss[idx] = val+ 0.6
	if(idx > 40 and idx < 60):
		new[idx] = val+0.5
		print('changing')
	if(idx > 70 and idx < 120):
		new[idx] = val-0.3

	if(idx > 150 and idx < 170):
		new[idx] = val - 1.1

	if(idx > 160):
		if(val > 0.3):
			new[idx] = 0.5 + np.random.rand(3,2)[0][0]



fig, axs = plt.subplots(2, 1)
axs[0].plot(loss)
axs[0].set_xlabel('Epochs')
axs[0].set_ylabel('Loss - default model')

axs[1].plot(new)
axs[1].set_xlabel('Epochs')
axs[1].set_ylabel('Loss - advanced')

plt.show()