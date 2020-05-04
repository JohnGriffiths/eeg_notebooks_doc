#!/usr/bin/env python
# coding: utf-8

# In[4]:


from muselsl import stream, list_muses, view, record
from multiprocessing import Process
from mne import Epochs, find_events
from time import time, strftime, gmtime
import os
from utils import utils
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')


# # Cueing
# 
# This notebook is slightly different than the PC notebooks due to differences in the Mac operating system.
# 
# First setup the computer by following the instructions in the mac_instructions_cueing.docx file, then return to this file.
# 
# The cueing task can ellicit a number of reliable changes. A central cue indicates the location of an upcoming target onset. Here the task can be changed to be perfectly predictive, or have some level of cue validity. Task is to indicate the orientation of a spatial grating on the target, up for vertical, right for horizontal.  
# 
# ERP - Validly cued targets ellict larger ERP's than invalidly cued targets
# 
# Response ERPs - Validly cued targets are more quickly identified and better identified
# 
# Oscillations - Alpha power lateralizes after a spatial cue onset preceeding the upcoming onset of a target. Alpha power becomes smaller contraleral to the target side, and larger ipsilateral with the target. 

# ## Step 1: Connect to an EEG Device
# 
# Make sure your device is turned on and run the following code. It should detect and connect to the device and begin 'Streaming...'
# 
# If the device is not found or the connection times out, try running this code again
# 
# If an error occurs scroll down, if it says BGAPIError, check that the black BLE dongle is pluged into the USB port, unplug the black BLE dongle and plug it back in again, then try again.

# In[5]:


# Search for available Muse devices
# muses = list_muses()
muses = list_muses()
print(muses)


# Now, choose the Muse you want to connect to. Check the ID on the side of your Muse device, and find the matching device in the list above and define the appropriate index in the my_muse_index variable. That is, if your Muse device is the first device listed above, the index is 1, if it is third in the list, the index is 3, etc.
# 
# If the connection is successful, the output will be:
# 
# `Connected to Muse: [your_muse_id]`  
# `Connected`  
# `Streaming ...`  
# 
# 
# If this doesn't work, try re-running the cell. You might also need to re-run the cell above. Just keep trying- it will work eventually! Sometimes it just takes time for the connection to be established.

# In[6]:


# Start a background process that will stream data from the first available Muse
# if the connection fails, run the list_muses cell above again

my_muse_index = 1

stream_process = Process(target=stream, args=(muses[my_muse_index-1]['address'],))
stream_process.start()


# ## Step 2: Apply the EEG Device and Wait for Signal Quality to Stabilize
# Open a new terminal by typing "command" + "T" at the same time.
# 
# Run the following to start the viewer and see the raw EEG data stream.
# 
# `conda activate nbmac`   
# `muselsl view --version 2`
# 
# The numbers on the side of the graph indicate the variance of the signal. Wait until this decreases below 10 for all electrodes before proceeding.

# ## Step 3: Run the Experiment
# 
# !!!MAKE SURE THE VOLUME IS ON AND TURNED UP TO FULL!!!
# 
# Modify the variables in the following code chunk to define how long you want to run the experiment (# of seconds) and the name of the subject and session you are running. 
# 
# Once you run the cell below, open a new terminal and run the following:
# 
# `cd ~/eeg-notebooks/notebooks`  
# `conda activate nbmac`
# 
# Then, paste the output from the cell below into the terminal and press `Enter`. This is the command to start the experiment, so make sure that the participant is seated in front of the computer at this point. Then have them quietly view the screen until the experiment is completed and do their best to minimize movement that might contaminate the signal. With their jaw and face relaxed, subjects should look directly at the flashing stimuli.
# 
# Data will be recorded into CSV files in the `eeg-notebooks/data/visual/cueing` directory
# 
# Here is an example of the experiment command for an cueing experiment that will last 120 seconds, for subject 1 and session 1: 
# 
# `python mac_run_exp.py --d 120 --s 1 --r 1 --e cueing`

# In[7]:


# Define these parameters 
duration = 240
subject = 100
session = 1
experiment = 'cueing'

# paste the output of this cell into the terminal
cmd2run = 'python mac_run_exp.py --d ' + str(duration) + ' --s ' + str(subject) + ' --r ' + str(session) + ' --e ' + experiment
print(cmd2run)


# ### Repeat Data Collection 2 times
# 
# Visualizing the effects can sometimes take many rounds of stimulus presentation. Depending on experimental conditions, this may require as little as one two minute trial or as many as 6. We recommend repeating the above experiment 2 times before proceeding. 
# 
# Make sure to take breaks, though! Inattention, fatigue, and distraction will decrease the quality of potentials such as the SSVEP

# ## Step 4: Prepare the Data for Analysis
# 
# Once a suitable data set has been collected, it is now time to analyze the data and see if we can identify the cueing effects
# 
# 
# ### Load data into MNE objects
# 
# [MNE](https://martinos.org/mne/stable/index.html) is a very powerful Python library for analyzing EEG data. It provides helpful functions for performing key tasks such as filtering EEG data, rejecting artifacts, and grouping EEG data into chunks (epochs).
# 
# The first step after loading dependencies is use MNE to read the data we've collected into an MNE `Raw` object

# In[1]:


from muselsl import stream, list_muses, view, record
from multiprocessing import Process
from mne import Epochs, find_events, concatenate_raws
from time import time, strftime, gmtime
import os
from stimulus_presentation import cueing
from utils import utils
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')


# In[9]:


sub = 104
raw = utils.load_data('visual/cueing', sfreq=256., 
                      subject_nb=sub, session_nb=1,
                      )
raw.append(
      utils.load_data('visual/cueing', sfreq=256., 
                      subject_nb=sub, session_nb=2,
                      )
           )


# ### Power Spectral Density
# 
# One way to analyze the SSVEP is to plot the power spectral density, or PSD. SSVEPs should appear as peaks in power for certain frequencies. We expect clear peaks in the spectral domain at the stimulation frequencies of 30 and 20 Hz.

# In[10]:


get_ipython().run_line_magic('matplotlib', 'inline')
raw.plot_psd();


# Should see the electrical noise at 60 Hz, and maybe a peak at the red and blue channels between 7-14 Hz (Alpha)

# ### Filtering
# 
# Most ERP components are composed of lower frequency fluctuations in the EEG signal. Thus, we can filter out all frequencies between 1 and 30 hz in order to increase our ability to detect them.

# In[11]:


raw.filter(1,30, method='iir')
raw.plot_psd(fmin=1, fmax=30);


# ### Epoching
# 
# Next, we will chunk (epoch) the data into segments representing the data 1000ms before to 2000ms after each cue, we will reject every epoch where the amplitude of the signal exceeded 100 uV, which should most eye blinks.

# In[15]:


events = find_events(raw)
event_id = {'LeftCue': 1, 'RightCue': 2}

rej_thresh_uV = 150
rej_thresh = rej_thresh_uV*1e-6

epochs = Epochs(raw, events=events, event_id=event_id, 
                tmin=-1, tmax=2, baseline=(-1, 0), 
                reject={'eeg':rej_thresh}, preload=True,
                verbose=False, picks=[0, 1, 2, 3])
print('sample drop %: ', (1 - len(epochs.events)/len(events)) * 100)

get_ipython().run_line_magic('matplotlib', 'inline')
conditions = OrderedDict()
conditions['LeftCue'] = [1]
conditions['RightCue'] = [2]

fig, ax = utils.plot_conditions(epochs, conditions=conditions, 
                                ci=97.5, n_boot=1000, title='',
                                diff_waveform=(1, 2))


# ### Spectrogram
# We can also look for SSVEPs in the spectrogram, which uses color to represent the power of frequencies in the EEG signal over time

# With this visualization we can clearly see distinct peaks at 30hz and 20hz in the PSD, corresponding to the frequency of the visual stimulation. The peaks are much larger at the POz electrode, but still visible at TP9 and TP10

# In[16]:


from mne.time_frequency import tfr_morlet
import numpy as np


frequencies =  np.linspace(6, 30, 100, endpoint=True)

wave_cycles = 6

 # Compute morlet wavelet

# Left Cue
tfr, itc = tfr_morlet(epochs['LeftCue'], freqs=frequencies, 
                      n_cycles=wave_cycles, return_itc=True)
tfr = tfr.apply_baseline([-1,-.5],mode='mean')
tfr.plot(picks=[0], mode='logratio', 
         title='TP9 - Ipsi');
tfr.plot(picks=[1], mode='logratio', 
         title='TP10 - Contra');
power_Ipsi_TP9 = tfr.data[0,:,:]
power_Contra_TP10 = tfr.data[1,:,:]

# Right Cue
tfr, itc = tfr_morlet(epochs['RightCue'], freqs=frequencies, 
                      n_cycles=wave_cycles, return_itc=True)
tfr = tfr.apply_baseline([-1,-.5],mode='mean')
tfr.plot(picks=[0], mode='logratio', 
         title='TP9 - Contra');
tfr.plot(picks=[1], mode='logratio', 
         title='TP10 - Ipsi');
power_Contra_TP9 = tfr.data[0,:,:]
power_Ipsi_TP10 = tfr.data[1,:,:]



# In[17]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as patches

# time frequency window for analysis
f_low = 7 # Hz
f_high = 10
f_diff = f_high-f_low
 
t_low = 0 # s
t_high = 1
t_diff = t_high-t_low

# Plot Differences
get_ipython().run_line_magic('matplotlib', 'inline')
times = epochs.times
power_Avg_Ipsi =   (power_Ipsi_TP9+power_Ipsi_TP10)/2;
power_Avg_Contra = (power_Contra_TP9+power_Contra_TP10)/2;
power_Avg_Diff = power_Avg_Ipsi-power_Avg_Contra;


#find max to make color range
plot_max = np.max([np.max(np.abs(power_Avg_Ipsi)), np.max(np.abs(power_Avg_Contra))])
plot_diff_max = np.max(np.abs(power_Avg_Diff))



#Ipsi
fig, ax = plt.subplots(1)
im = plt.imshow(power_Avg_Ipsi,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', cmap='coolwarm', vmin=-plot_max, vmax=plot_max)
plt.xlabel('Time (sec)')
plt.ylabel('Frequency (Hz)')
plt.title('Power Average Ipsilateral to Cue')
cb = fig.colorbar(im)
cb.set_label('Power')
# Create a Rectangle patch
rect = patches.Rectangle((t_low,f_low),t_diff,f_diff,linewidth=1,edgecolor='k',facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)

#TP10
fig, ax = plt.subplots(1)
im = plt.imshow(power_Avg_Contra,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', cmap='coolwarm', vmin=-plot_max, vmax=plot_max)
plt.xlabel('Time (sec)')
plt.ylabel('Frequency (Hz)')
plt.title(str(sub) + ' - Power Average Contra to Cue')
cb = fig.colorbar(im)
cb.set_label('Power')
# Create a Rectangle patch
rect = patches.Rectangle((t_low,f_low),t_diff,f_diff,linewidth=1,edgecolor='k',facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)

#difference between conditions
fig, ax = plt.subplots(1)
im = plt.imshow(power_Avg_Diff,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', cmap='coolwarm', vmin=-plot_diff_max, vmax=plot_diff_max)
plt.xlabel('Time (sec)')
plt.ylabel('Frequency (Hz)')
plt.title('Power Difference Ipsi-Contra')
cb = fig.colorbar(im)
cb.set_label('Ipsi-Contra Power')
# Create a Rectangle patch
rect = patches.Rectangle((t_low,f_low),t_diff,f_diff,linewidth=1,edgecolor='k',facecolor='none')
# Add the patch to the Axes
ax.add_patch(rect)




# We expect greater alpha power ipsilateral to the cue direction (positive values) from 0 to 1.5 seconds

# ### Target Epoching
# 
# Next, we will chunk (epoch) the data into segments representing the data .200ms before to 1000ms after each target, we will reject every epoch where the amplitude of the signal exceeded ? uV, which should most eye blinks.

# In[30]:


events = find_events(raw)
event_id = {'InvalidTarget_Left': 11, 'InvalidTarget_Right': 12,
           'ValidTarget_Left': 21,'ValidTarget_Right': 11}

epochs = Epochs(raw, events=events, event_id=event_id, 
                tmin=-.2, tmax=1, baseline=(-.2, 0), 
                reject={'eeg':.0001}, preload=True,
                verbose=False, picks=[0, 1, 2, 3])
print('sample drop %: ', (1 - len(epochs.events)/len(events)) * 100)

get_ipython().run_line_magic('matplotlib', 'inline')
conditions = OrderedDict()
conditions['ValidTarget'] = [21,22]
conditions['InvalidTarget'] = [11,12]

fig, ax = utils.plot_conditions(epochs, conditions=conditions, 
                                ci=97.5, n_boot=1000, title='',
                                diff_waveform=(1, 2))

