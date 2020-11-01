# Freeze_detection
Script to detect freezes in a video
Author: Mohamed Aous KHADHRAOUI @SeaOwl France
Last Update: 29/06/2020

This document is to explain how to run freeze_detection script with user
parameters then explains different configuration parameters

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
How to run the script:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

---------------------------Environment specs-------------------------------------

This script is ideally run with Python 3 compiler
Libraries to be installed with python
	- opencv-python (supports older versions)
	- scikit-image
PS: Installing both of these completely, ensures the installation of the rest 
the libraries

------------------------Basic how to run the script on a video-------------------

In a terminal type in:
python \PATH_TO\freeze_detection.py PATH_TO_VIDEO

PATH_TO_VIDEO is either:
- A path to a folder containing video files (script
will output a csv file containing all freezes encountered in all videos)
- Or a path to a single video file



Running this will ensure default run of the script on a video and outputs a csv
log file specifying freezes of more than 1s encountered while parsing the video.

---------------------------------------------------------------------------------

PS: video can be live streaming or pre-taped/ supports all common video types
(.mp4, .mov) but should include AVI
   script comes with test videos under directory "Test videos"
run in terminal as example of test:

---------------------------------------------------------------------------------
python freeze_detection.py "Test videos\15 Fps 1600X900.mp4" -Test True
---------------------------------------------------------------------------------


######## User parameters ##########

To see all the parameters meant for the end user type in the terminal:
python \PATH_TO\freeze_detection.py --help

Running this should output:
---------------------------------------------------------------------------------

usage: freezevideo.py [-h] [-log_path [LOG_PATH]] [-quality] [-thres [THRES]]
		      [-frame_affinity [FRAME_AFFINITY]]
                      [-Test [TEST]] [-reduction [REDUCTION]]
                      path

logs all frame freezes in a video

positional arguments:
  path                  video path

optional arguments:

  -h, --help            show this help message and exit
  -log_path [LOG_PATH]  log file's path
  -quality, --quiet
  -thres [THRES]        noise threshold
  -frame_affinity [FRAME_AFFINITY]
                        freeze detection affinity in seconds
  -Test [TEST]          test mode
  -reduction [REDUCTION]
                        reduce resolution
			
--------------------------------------------------------------------------------

######## Default values of user parameters #########

(In case options are not specified)
-log_path: by default location of log file is in the same root directory of the
		script
-quality: by default script runs with fast mode and quality mode makes script
		slower (may affect performance in a live streaming video)
-thres: by default noise threshold is calculated dynamically, using this option
	makes this threshold static
-frame_affinity: by default script only detects freezes of more than 1s (threshold
	limit = 0.5s) and less than 30s
-test: by default script runs without test mode on (passing this variable to true
	outputs time perfomance and draws graph of encountered freezes)
-reduction: by default script reduces input resolution higher than some
	threshold determined by constructor

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may edit configuration file: "freeze_config.py" in case performance of the 
script is not optimal for tests of validation.
Under appli:
	you can change default values of user parameters
Under img_res:
	in resolution reduction mode serves as a cap for video resolution intake
	(ensures stable performance for different input resolutions)
Under freeze:

###################### noise_verification_fact #################################

factor between threshold of freeze and threshold of verification
should ideally be between 5 and 20 for usual fps videos

########################## noise_factor ########################################

factor of noise between video with no freeze and video with freeze
should ideally be between 10 and 100 for usual comressed video qualities

############################## freq ############################################

frequency of noise_threshold update in seconds
should not be under 0.5s
upper bound depends on application (can be set higher if video's environment does
not vary much)
