#Date 21/06/2020
#program for freeze detection
#Author : Aous KHADHRAOUI

def get_time_format(t):
    return(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))
    
def detect_freeze(args, v_path = None):
    base=os.path.basename(args.path)
    if v_path != None:
        base=os.path.basename(v_path)
    fname = os.path.splitext(base)[0]
    print("Processing: ", fname)

    #resolution reduction
    resol = (img_res['X'],img_res['Y'])

    try:
        if v_path != None:
            video = cv2.VideoCapture(v_path)
        else:
            video = cv2.VideoCapture(args.path)
    except:
        print("Wrong video path")
        return(0)

    #length of video
    length = video.get(cv2.CAP_PROP_FRAME_COUNT)

    #First frame
    _, frame0 = video.read()
    try:
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    except:
        print("Wrong video path")
        return(0)
    if args.reduction:
        if frame0.shape[1] > resol[0] or frame0.shape[0] > resol[1]:
            frame0 = cv2.resize(frame0, resol)
    previous_frame = np.asarray(frame0)/255

    try:
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', fname)
        file_date = datetime.strptime(match.group(), '%Y-%m-%d-%H-%M-%S')
        start_time = time.mktime(file_date.timetuple())
    except:
        start_time = os.path.getctime(args.path)
    if args.Test:
        start_test_time = time.time()

    log.write ("Start_time: "+ fname + ","+ get_time_format(start_time)+ ",_" "\n")

    #freeze frame counter and frame counter
    ff_count = 0
    f_count = -1
    

    #Determine fps
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = int(video.get(cv2.cv.CV_CAP_PROP_FPS))
    else:
        fps = int(video.get(cv2.CAP_PROP_FPS))
    
    #Maximum freeze frame duration
    ff_count_cap = freeze['ff_count_cap']*fps

    #Define threshold for frames and noise
    frame_thres = int(fps*args.frame_affinity)-1
    noise_thres = args.thres
    recover_noise_thres = noise_thres

    #make sure the freeze stopped
    verification_thres = int(fps/freeze['noise_verification_fact'])
    verification_count = 0

    #number of frames to define noise thres
    nb_thres = int(fps/2)

    #frequency of noise thres update
    noise_thres_update_freq = freeze['freq']*fps
    noise_factor = freeze['noise_factor']

    

    structural = args.quiet
    
    if args.Test:
        L = []
        V = []
        seconds = []

    mean = 0
    counter_mean = 0
    while(True):

        #Next frame
        r_, frame = video.read()
        f_count +=1
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if args.reduction:
                if frame.shape[1] > resol[0] or frame.shape[0] > resol[1]:
                    frame = cv2.resize(frame, resol)
        except:
            if ff_count > frame_thres:
                endtime = starttime + ff_count/fps
                log.write(get_time_format(endtime)+","+str(round(endtime - starttime, 1))+" \n")
            print("Processing ", f_count/fps, "th second...          [", 100,"%]",   end = "\r")
            print("\n Finished video")
            break

        current_frame = np.asarray(frame)/255


        #Calculate difference between current and previous frame
        if structural:
            diff = 1- compare_ssim(frame, frame0) 
        else:
            diff = np.mean(np.absolute(current_frame - previous_frame)**2)

        #Determine noise threshold
        if args.thres == 0:
            if ((f_count % noise_thres_update_freq) < nb_thres) and ff_count == 0:
                mean += diff/nb_thres
                counter_mean += 1
                print("Processing %.2f"  %(f_count/fps) + "th second...          [", int(f_count*100/length),"%]",   end = "\r")
            else:
                counter_mean = 0
                mean = 0
            if counter_mean == nb_thres:
                if noise_thres:
                    recover_noise_thres = noise_thres
                noise_thres = mean / noise_factor
                
                #if noise thres is too big we stay at previous threshold
                if recover_noise_thres:
                    if noise_thres > (1 + freeze['unbounded_noise_thres'])*recover_noise_thres:
                        noise_thres = recover_noise_thres
        

        #log status to file
        if (diff < noise_thres):
            if ff_count >= frame_thres:
                if ff_count == frame_thres:
                    starttime = start_time + (f_count - frame_thres)/fps
                    log.write(fname + ',')
                    log.write(get_time_format(starttime) + ",")
                if ff_count >= verification_thres:
                    verification_count = 0
            ff_count +=1
        else:
            if ff_count >= verification_thres:
                verification_count+=1
                if ff_count < frame_thres:
                    ff_count +=1
            if verification_count == verification_thres or verification_count == verification_thres+1:
                if ff_count > frame_thres:
                    endtime = starttime + ff_count/fps
                    log.write(get_time_format(endtime)+","+str(round(endtime - starttime, 1))+" \n")
                ff_count = 0
                verification_count = 0

        #update previous frame
        previous_frame = current_frame
        frame0 = frame
        
        #bug detection
        if ff_count >= ff_count_cap:
           noise_thres = recover_noise_thres
           ff_count = 0
           verification_count = 0
        	
        #print(diff, noise_thres)
        if args.Test:
            seconds.append(f_count/fps)
            if ff_count > verification_thres:
                V.append(1)
                if ff_count > frame_thres:
                    L.append(1)
                else:
                    L.append(0)
            else:
                V.append(0)
                L.append(0)

    video.release()
    cv2.destroyAllWindows()
    if args.Test:
        
        print("Freeze detection took: ", time.time() - start_test_time, " seconds\n")
        plt.plot(seconds, V)
        plt.plot(seconds, L)
        plt.show()

if __name__ == '__main__':
    import argparse
    from freeze_config import *

    parser = argparse.ArgumentParser(description="logs all frame freezes in a video")
    parser.add_argument("path", type = str, help="video path" )
    parser.add_argument("-log_path", type = str, help="log file's path",
    				nargs='?',  default =appli['log_filepath'])
    parser.add_argument("-quality", "--quiet", action="store_true")
    parser.add_argument("-thres", type = float, help = "noise threshold",
    				 nargs = '?', default = appli['threshold'])
    parser.add_argument("-frame_affinity", type = float,
    			 help = "freeze detection affinity in seconds",
    			 nargs = '?', default = appli['frame_affinity_sec'])
    parser.add_argument("-Test", type = bool, help = "test mode",
    				 nargs = '?', default = appli['test_mode'])
    parser.add_argument("-reduction", type = bool, help = "reduce resolution",
    				 nargs = '?', default = appli['reduction'])

    args = parser.parse_args()
    print("Arguments passed successfully")
    if args.Test:
        fig = plt.figure(1)

    #log file
    try:
        log = open(args.log_path, 'w')
    except:
        print("\n Please verify that log file is closed before executing process ! \n")
        quit()
        
    log.write ("video_name,freeze_start,freeze_stop,duration\n")

    if os.path.isfile(args.path):
        detect_freeze(args)
    else:
        for filename in os.listdir(args.path):
            directory = args.path[:] + "/"
            detect_freeze(args, v_path = directory +  filename)

    log.close()
    print("Process Finished")

