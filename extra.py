# -*- coding: utf-8 -*-
"""
Version: 2019.02.0

The ppc module (ppc is short for "PsychoPy Course) contain some useful
methods to help you build and verify your experiment. Put the ppc.py
in the same folder as your script or in your PYTHONPATH. See these
functions in use in the ppc3_template.py and in ppc2_timing.py.

Jonas Lindeløv

TO DO:
 * add UTC times in csvWriter?
 * Remove sound or make it a dummy-one which drops back to psychopy
 * Use PEP8 names instead of camelCase
"""

# Check python version
import sys
python3 = sys.version_info[0] == 3


def deg2cm(angle, distance):
    """
    Returns the size of a stimulus in cm given:
        :distance: ... to monitor in cm
        :angle: ... that stimulus extends as seen from the eye

    Use this function to verify whether your stimuli are the expected size.
    (there's an equivalent in psychopy.tools.monitorunittools.deg2cm)
    """
    import math
    return math.tan(math.radians(angle)) * distance  # trigonometry


class csv_writer(object):
    def __init__(self, filename_prefix='', folder='', column_order=[]):
        """
        Take a dictionary and write it to a csv file as a row.
        Writing is very fast - less than a microsecond.

        :filename_prefix: (str) would usually be the id of the participant
        :folder: (str) optionally use/create a folder.
        :column_order: (list) The columns to put first in the csv. Some or all.

        Use like:

            # Once towards the beginning of the script
            writer = csv_writer('participant1', folder='data', column_order=['id', 'condition'])

            # After each trial is completed
            trial = {'id': 'participant1', 'rt': 0.2323, 'condition': 'practice'}
            writer.write(trial)

            # Optional: forces save of hitherto collected data to disk.
            # writer.flush()
        """

        import os
        import time

        self.column_order = column_order
        self._header_written = False

        # Create folder if it doesn't exist
        if folder:
            folder += '/'
            if not os.path.isdir(folder):
                os.makedirs(folder)

        # Generate self.save_file and self.writer
        # Filename for csv. E.g. "myFolder/subj1_cond2 (2013-12-28 09-53-04).csv"
        self.save_file = '%s%s_%s.csv' % (folder, filename_prefix, time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()))
        self._setup_file()

    def _setup_file(self):
        """Setting up the self.writer depends on python version."""
        import csv

        if python3:
            self._file = open(self.save_file, 'a', newline='')
        else:
            self._file = open(self.save_file, 'wb')

        self.writer = csv.DictWriter(self._file, fieldnames=self.column_order)  # The writer function to csv. It appends a single row to file

    def write(self, trial):
        """Saves a trial to buffer. :trial: a dictionary"""
        # Write header and add fieldnames on first trial
        if self.writer.fieldnames is None:
            self.writer.fieldnames = list(trial.keys())

        # Check that all column_order are present in the trial
        if len(set(self.column_order) - set(list(trial.keys()))) != 0:
            raise(ValueError('A column in column_order was not present in the trial dictionary'))

        # Enforce order on first columns. Then add the last in "random" order.
        if len(trial) > len(self.column_order):
            self.writer.fieldnames = self.column_order + list(set(list(trial.keys())) - set(self.column_order))

        # Write header if it hasn't been
        if not self._header_written:
            self.writer.writeheader()
            self._header_written = True

        # Now write data
        self.writer.writerow(trial)  # Works both in python2 and python3

    def flush(self):
        """Saves current content to file.
        This will happen automatically when the script terminates.
        Only do this if you fear a hard crash. It's mostly fast (< 1 ms) but can be slow (up to 30 ms)
        """
        self._file.close()
        self._setup_file()
