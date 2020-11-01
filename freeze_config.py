#Libraries
import cv2
import numpy as np
import time
import random
from skimage.measure import compare_ssim
from skimage.measure import compare_mse
import argparse
import matplotlib.pyplot as plt
import os
import sys
import re
from datetime import datetime


#configutraion parameters file
appli={
    'log_filepath':os.path.dirname(__file__)+"/freeze_log.csv",
    'threshold':0,
    'frame_affinity_sec':1,
    'test_mode':False,
    'reduction':True
}

#if reduction: reduces input resolution to following
img_res={
    'X':800,
    'Y':640
}

#noise_verification_fact: factor of time between threshold of freeze and threshold of verification
#noise_factor: factor of noise between video with no freeze and video with freeze
#freq: frequency of noise_threshold update in seconds
#ff_count_cap: maximum freeze duration in seconds
#unbounded_noise_thres: if noise_thres is bigger than 100*(1 + unbounded_noise_thres)% the value
	#of the previous threshold, noise thres doesn't get updated
freeze={
    'noise_verification_fact':5,
    'noise_factor':5,
    'freq':0.9,
    'ff_count_cap':30,
    'unbounded_noise_thres':0.4
}
