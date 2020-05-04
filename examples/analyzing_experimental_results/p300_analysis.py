"""
P300 Analysis Only
===============================

This notebook runs only the data analysis part of N170 notebook.

Look at the notes to see how this can be run on the web with binder or google collab.

All of the additional notes are removed; only the code cells are kept.

"""

###################################################################################################

# Imports
from muselsl import stream, list_muses, view, record
from multiprocessing import Process
from mne import Epochs, find_events
from time import time, strftime, gmtime
import os
#from stimulus_presentation import n170
#os.chdir('../')
from eegnb.analysis import utils
#;from utils import utils
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')


###################################################################################################
# Next header
# ---------------------------------
#
#
# Step 1: Connect to an EEG Device 

# Step 2: Apply the EEG Device and Wait for Signal Quality to Stabilize  

# Step 3: Run the Experiment  

blah blah

blah 

blah

###################################################################################################
# Next header
# ---------------------------------
#
#
# Step 1: Connect to an EEG Device


blah blah

blah

blah

###################################################################################################
# Next header
# ---------------------------------
#
#
# Step 1: Connect to an EEG Device

blah blah

blah 

blah
