import random
import csv
import config
from collections import defaultdict

# parameters to generate an experiment
# color_dict_path = '/Users/john/Desktop/School/TMU/Courses/color.csv'
# words_dict_path = '/Users/john/Desktop/School/TMU/Courses/words.csv'
# # define number of blocks
# num_of_blocks = 3
# #define number of condition presented per block, assume balanced design (if 2, then 2 neutral)
# num_of_conds = 5
# #1 for congruent condition, 2 for incongrunent condition, 3 for neutral
# num_of_trials = num_of_conds*3 #times 3 because three conditions

def gen_dict(path): #note: rgb colors are stored as a string inside a list. need to [0]
    """
    :param path: given path to csv file
    :return: dictionary where first column stores keys, second column stores values
    """
    result = {}
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line = 0
        for row in reader:
            if line == 0:
                line +=1
            else:
                id = row[0]
                value = row[1]
                result.setdefault(id, [])
                result[id].append(value)
    return result

def gen_rand_color(color_list, current_color=None):
    """
    CURRENTLY DEPRECATED
    :param color_list: a list of color options
    :param current_color: if want to select a random color that is not the current one
    :return: a random color from color_list
    """
    clist = color_list.copy()
    if current_color:
        clist.remove(current_color)
    return random.choice(clist)


def gen_trial(block, trial, cond, word, color):
    """
    CURRENTLY DEPRECATED
    :param block:
    :param trial:
    :param cond:
    :param word:
    :param color:
    :return:
    """
    colors = words_dict['color']
    words = words_dict['neutral']
    c_len = len(colors) - 1
    c = colors[random.randint(0, c_len)]
    # check if the current color is the same as previous two stimuli's colors
    # swap if so
    if prev_c:
        if c == prev_c[0] and c == prev_c[1]:
            c = gen_rand_color(colors, c)

    if cond == 1:  # (congruent)
        w = c

    elif cond == 2:  # (incongruent)
        w = gen_rand_color(colors, c)  # generate incongruent color

    else:  # entry == 3 (neutral)
        w = words[random.randint(0, c_len)]

    results = {'block_index': block,
               'trial_index': trial,
               'condition': cond,
               'word': w,
               'color': c,
               'RGB': color_dict[c][0]
               }

    return results


def gen_pool(color_dict, words_dict):
    """
    returns a dictionary of 'congruent', 'incongruent' and 'neutral'
    each containing tuples of (word, color)
    """
    results = defaultdict(list)

    con_rep_times = len(color_dict) - 1  # this is because incongruent will have n(n-1) combinations
    for color in color_dict:
        # congruent conditions
        results['congruent'].append((color, color))
        # incongruent conditions
        for c in color_dict:
            if c is not color:
                results['incongruent'].append((c, color))
        # neutral conditions
        for w in words_dict['neutral']:
            results['neutral'].append((w, color))
    results['congruent'] = results['congruent']*con_rep_times
    for r in results:
        random.shuffle(results[r])
    return results

def gen_list(color_dict_path, words_dict_path, config):
    """
    Generates the entire experimental paradigm according to config
    :param color_dict_path: str
    :param words_dict_path: str
    :param config: .py file containing all experimental parameters
    :return: 2D list of blocks in dim 1 and trials per block in dim 2. Each entry is then a dict of trial info
    """
    #global color_dict
    color_dict = gen_dict(color_dict_path)
    #global words_dict
    words_dict = gen_dict(words_dict_path)
    results_blocks = []
    conds = ['congruent','incongruent','neutral']*config.num_of_conds
    pool = gen_pool(color_dict, words_dict)
    pool_size = len(pool['congruent'])*len(pool.values())
    tot_trial = 0
    for block_num in range(0,config.num_of_blocks):
        random.shuffle(conds)
        trial_num = 0
        results = []
        for cond in conds:
            tot_trial += 1
            ## check if pool is depleted
            if tot_trial == pool_size:
                pool = gen_pool(color_dict, words_dict)
                tot_trial = 0
            curr = pool[cond].pop() # curr = (word, color)
            trial_info = {'block_index': block_num,
                       'trial_index': trial_num,
                       'condition': cond,
                       'word': curr[0],
                       'color': curr[1],
                       'RGB': color_dict[curr[1]][0]
                       }
            trial_num+=1
            results.append(trial_info)
        results_blocks.append(results)
    return results_blocks

# final = gen_list(color_dict_path, words_dict_path, config)
# print(final)
# print(len(final[0]))