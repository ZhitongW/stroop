import os

# parameters to generate an experiment
pwd = os.getcwd()
color_dict_path = pwd+'/color.csv'
words_dict_path = pwd+'/words.csv'
# define number of blocks
num_of_blocks = 3
#define number of condition presented per block, assume balanced design (if 2, then 2 neutral)
num_of_conds = 15 ## HAS TO BE [15, 30]
#1 for congruent condition, 2 for incongrunent condition, 3 for neutral
num_of_trials = num_of_conds*3 #times 3 because three conditions

# Visual parameters
IBI = 2
VISUAL_DUR = 0.5 #stimulus presented for 1300 msec (Potenza et al., 2003)
VISUAL_ISI = 3
VISUAL_JITTER = [0.05, 0.1, 0.15, 0.2] #randomly choose jitter time each trial

# Monitor parameters
MON_DISTANCE = 60             # Distance between subject's eyes and monitor
MON_WIDTH = 50                # Width of your monitor in cm
#MON_SIZE = [1920, 1080]        # Pixel-dimensions of your monitor
MON_SIZE = [800, 600]        # Pixel-dimensions of your monitor
SAVE_FOLDER = 'log'           # Log is saved to this folder. The folder is created if it does not exist.

# Window parameters
MESSAGE_POS = [0, 3]   # [x, y]
STIM_HEIGHT = 15     # Height of the text, still in degrees visual angle
MESSAGE_WIDTH = 35
PROMPT_HEIGHT = 1
FIX_HEIGHT = 15
# KeyPress Setup
KEYS_QUIT = ['escape'] # Keys that quits the experiment
COND_KEYS = ['space']