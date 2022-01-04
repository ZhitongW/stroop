import config, extra, random, instruct
from list_generation import gen_list

blocks = gen_list(config.color_dict_path, config.words_dict_path, config)
debug = False
eeg = False
from psychopy import core, visual, gui, monitors, event
from psychopy.hardware import keyboard

## Set up demo
demo = {"subject":"", "age":"", "gender":["male", "female"]}
if not gui.DlgFromDict(demo, order = ["subject", "age", "gender"]).OK:
    core.quit()

## Set up time
glob_t = core.Clock()
trial_t = core.Clock()
rt_t = core.Clock()

## Set up log
sub_id = "sub-"+str(demo["subject"])
log = extra.csv_writer(sub_id,folder = config.SAVE_FOLDER,
                           column_order = ["block_index", "trial_index",
                                           "condition", "word", "color", "RGB"])

## Create window ##
""" Create monitor object, using width and distance to control for control
 size of stimulus in degrees.
"""
exp_mon = monitors.Monitor("testMonitor", width = config.MON_WIDTH,
                           distance = config.MON_DISTANCE)
exp_mon.setSizePix(config.MON_SIZE)

## Initiate Window
"""
TODO: Change monitor size to be larger and more in the center
TODO: Sound recording
TODO: Send pull request to Paul
"""
# using the exp_mon object above, and use degree as units.
win = visual.Window(monitor = exp_mon, units = "deg", fullscr = True ,
                    allowGUI = False, color = "black")

## Stimulus
# Setup each present stimulus before experiment began
# Fixation cross is just the character "+".
fix = visual.TextStim(win, "+", height=config.FIX_HEIGHT)
# Stimulus state
# TODO: FIX CENTERING PROBLEM
stim_text = visual.TextStim(win, height = config.STIM_HEIGHT, pos=(0,0),
                            anchorHoriz='center', anchorVert='center',
                            wrapWidth = config.MESSAGE_WIDTH)


###################
## (2).Functions ##
###################
def pp_reset(eeg):
    if eeg:
        pp.setData(0)

def keypress(config):
    """Keypress for the experiment
    Accepts only responds and quit keys set in the configuration file
    and if quit key is accepted, close out the window.
    input:
        config  : config.py
    return
        key     : Key press being pressed
    """
    ## Responds configuration ##
    resp_keys = config.RESPS
    resp_keys += config.KEYS_QUIT

    # add in lowercase
    resp_keys += config.RESPS_L

    # Key press
    key = event.getKeys(keyList = resp_keys)

    # Quit everything if quit key was pressed
    # *Note: In this case is "escape" key
    if config.KEYS_QUIT[0] in key:
        log.flush() # Close the file if quit-key is pressed.
        core.quit()

    return key

def prompt(text = "", keyList=None):
    """Present instruction prompt.
    Shows instruction and returns answer (keypress) and reaction time.
    Defaults is no text and accept all keys.
    input:
        text: text wanted to present.
        keyList: list of keys that it will accept to break out of prompt,
                 if not specified, will accept all keys.

    results:
        Present the screen with prompt given.
    """
    # Draw the TextStims to visual buffer
    # then show it and reset timing immediately (at stimulus onset)
    prompt_text = visual.TextStim(win, height = config.PROMPT_HEIGHT,
                            wrapWidth = config.MESSAGE_WIDTH)
    prompt_text.text = text
    prompt_text.wrapwidth = True
    prompt_text.font = "Arial"
    prompt_text.antialias = True

    # Stimulus present
    prompt_text.draw()
    time_flip = win.flip()

    # Halt everything and wait for the first responses matching the
    # keys given in the KeyList object
    if keyList:
        keyList += config.KEYS_QUIT

    # There is key time here, may adjust the function to get key time.
    key, time_key = event.waitKeys(keyList = keyList, timeStamped = True)[0]

    # Quit everything if quit key was pressed
    # Note: In this case is "escape" key
    if key in config.KEYS_QUIT:
        log.flush() # Close the file if quit-key is pressed.
        core.quit()

def block_prompt(blocks, bn, config):
    """ Experimental block prompt presentation.
    Function initiate experimental instruction prompts for beginning of each block
    for subject to read.

    Input:
        blocks : A list of list of dictionary with conditions and trial information
        bn     : Python's loop block number i.e 0,1,2,3,4...etc
        config : configuration file with all specific experimental definition

    --------------------------------------------------------
                        Presenting
    --------------------------------------------------------
    bottom      :   Press SPACEBAR to begin the next block.
    --------------------------------------------------------
    """
    # General text
    block_break = visual.TextStim(win, text="press SPACE keys to continue...",
                                  pos = (0, 0),antialias = True)
    ## commenting below because no user response
    # left_resp_key = visual.TextStim(win, text=f"Press {config.RESPS[0]} ",
    #                                 font = "Arial", pos = (-5, -1),
    #                                 antialias = True)
    # right_resp_key = visual.TextStim(win, text=f"Press {config.RESPS[1]} ",
    #                                  font = "Arial", pos = (5, -1),
    #                                  antialias = True)
    # left_resp_stim = visual.TextStim(win, font = "Arial",pos = (-5, 1),
    #                                  antialias = True)
    # right_resp_stim = visual.TextStim(win, font = "Arial", pos = (5, 1),
    #                                   antialias = True)

    # Responds position
    # if (blocks[bn][0]['common_stim'] == 'O') and (blocks[bn][0]['common_resp'] == 'J'):
    #     left_resp_stim.text = f" {blocks[bn][0]['common_stim']}"
    #     right_resp_stim.text = f" {blocks[bn][0]['rare_stim']}"
    # else:
    #     left_resp_stim.text = f" {blocks[bn][0]['rare_stim']}"
    #     right_resp_stim.text = f" {blocks[bn][0]['common_stim']}"

    # Draw all items
    block_break.draw()
    # left_resp_stim.draw()
    # right_resp_stim.draw()
    # left_resp_key.draw()
    # right_resp_key.draw()
    time_flip = win.flip()

    # Halt everything and wait for a response matching the keys
    # given in the Q object.
    key, time_key = event.waitKeys(keyList = config.COND_KEYS,
                                   timeStamped = True)[0]

    # Look at first reponse [0]. Quit everything if quit-key was pressed
    if key in config.KEYS_QUIT:
        log.flush()
        core.quit()
    return

def run_block(blocks, bn, config):
    """ Experimental block
    Taking in blocks and it current block number. Loop around list of dictionary,
    execute each trials in following column_order

    Block Executing Order
    1. Start with Inter-block Interval
    2. Loop around whole a block of trials
        - ISI
        - stimulus on
        - Respond on
        - Log

    Input:
        blocks      : a list of list of dictionary with trial information
        bn          : block number
        config      : config.py with all specific configuration variables
        eeg         : Boolean value, if true setup parallel port.
    """
    # 1.Start fixation for Inter block interval.
    fix.draw()
    win.flip()
    core.wait(config.IBI) # Wait before experiment begins.


    for tr in range(config.num_of_trials):
        # Start trial timer, also reset timer for intra-trial RT
        if debug:
            print(f"Block {bn} Trial {tr} ...")
        tr_glob_time = glob_t.getTime()
        trial_t.reset()

        ## stimulus On ##
        ## DO I HAVE TO DO IT FRAME BY FRAME?


        # add jitter
        isi_dur = config.VISUAL_ISI + random.choice(config.VISUAL_JITTER)
        stim_text.text = blocks[bn][tr]["word"]
        stim_text.color = eval(blocks[bn][tr]["RGB"])
        stim_text.draw()
        # stim on
        win.flip()
        stim_on = trial_t.getTime()
        core.wait(config.VISUAL_DUR)
        # stim off
        fix.draw()
        win.flip()
        ## Inter Stimulus Interval (ISI) ##
        rt_t.reset()
        isi = trial_t.getTime()
        wait_keys = config.COND_KEYS + config.KEYS_QUIT
        key_time = event.waitKeys(maxWait=isi_dur, keyList=wait_keys, timeStamped=rt_t)
        press_glob_time = glob_t.getTime()

        if key_time:
            key_time = key_time[0]
            if config.KEYS_QUIT[0] in key_time[0]:
                log.flush()  # Close the file if quit-key is pressed.
                core.quit()

            rt = key_time[1]
            trial_log = dict(trial_num=tr + 1,
                             block_num=bn + 1,
                             press_glob_time=press_glob_time,
                             rt=rt,
                             stim_on=stim_on,
                             isi=isi_dur,
                             glob_init_time=tr_glob_time
                             )
        else: #no key pressed
            trial_log = dict(trial_num=tr + 1,
                             block_num=bn + 1,
                             press_glob_time=None,
                             rt=None,
                             stim_on=stim_on,
                             isi=isi_dur,
                             glob_init_time=tr_glob_time,
                             )
        tri_info = blocks[bn][tr]
        tri_info.update(trial_log)
        log.write(tri_info)
        #make sure that the full isi is carried out
        if (trial_t.getTime() - isi) < isi_dur:
            core.wait(isi_dur-(trial_t.getTime() - isi))



def exp(blocks, config, glob_t, instruct):
    """Execute the Experiment
    Input:
        blocks   : A list of list of dictionary with conditions and trial information
        config   : Configuration file with all specific experimental definition
        glob_t   : Global rt_t
        instruct : Instruction files with all the prompt instructions

    Experiment flow:
        -   Instructions
            -   Initial instruction
            -   Familarized sample stimulus
            -   Final instructions before experiment begin
        -   Execute formal experimental
    """
    exp_bg = glob_t.getTime()
    print(f"Experiment began machine time : {exp_bg} ...")

    ## Instructions ##
    prompt(instruct.init_inst)


    # Final instructions before experiment start
    prompt(instruct.final_inst)

    # EEG PIN setup
    if eeg:
        if debug:
            print(f" BLOCK BEGAN : {glob_t.getTime()}")
        pp.setData(config.INIT_PIN)

    ## Initate Experimental ##
    for bn in range(len(blocks)):
        block_prompt(blocks, bn, config)
        # Beginning of each block
        if eeg:
            pp.setData(config.BB_PIN)
        run_block(blocks, bn, config)

    # EEG PIN setup
    if eeg:
        pp.setData(config.END_PIN)
        if debug:
            print(f" BLOCK ENDED : {glob_t.getTime()}")

    # Experiment End prompt
    prompt(instruct.finished_inst)

###########################
## (3).Excute Experiment ##
###########################
if __name__ == "__main__":
    # Run Experiment
    exp(blocks, config, glob_t, instruct)
    # debug
    if debug:
        exp_end = glob_t.getTime()
        print(f" Total Experimental Run time began : {mm_time} \n End : {exp_end}")
