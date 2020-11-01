import time
import keyboard
import os
import cv2
import pandas as pd
import shutil
import Functions


#When Program Starts
init_time = time.time()
path = os.getcwd() + "\\"

#Live stream of 1s and 0s every
def record_data(dir,audio):
    list = os.listdir(dir)      # dir is your directory path
    start_time = time.time()
    end_time = start_time + audio.audio_length()
    ideal_seconds = 0.1
    seconds = 0.1 # current spot
    filler = 0
    filler_prev = 0
    data= [[], []]
    error = 0
    i = 0


    while start_time < end_time:

        #appends filler and start_time to  the beginning of the list.
        data[0].append(filler)
        data[1].append(start_time)

        if seconds > 0:
            error += (data[1][i] - data[1][i-1] - ideal_seconds)

        # If a keyword has been said reset filler to 0
        if filler != 0:
            print(filler)
            filler = 0

        #On button  press change the stream of outgoing 0s to 1s and change 1s to 0s.
        elif keyboard.is_pressed("U"): # uhhhh
            filler = 1
        elif keyboard.is_pressed("M"): # ummmm
            filler = 2
        elif keyboard.is_pressed("L"): # like
            filler = 3

        #Loop designed to slow the program down to 10 iterations per second.
        while True:
            current_time = time.time()
            if start_time + seconds <= current_time:
                break

        #print(error)
        if error >= ideal_seconds:
            data[0].append(filler)
            data[1].append(start_time)
            i += 1
            error -= ideal_seconds
            seconds = seconds*0.998
            #print("Positive correction error when i=" + str(i))

        elif error <= -1*ideal_seconds:
            time.sleep(abs(error))
            #print("Negative correction error when i=" + str(i))
            seconds = seconds*1.002


        start_time = time.time()
        i += 1
    return data


#Takes a list of lists and writes  it to a csv file.
def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data[0])):
            file.write("{},{}\n".format(data[0][x],data[1][x]))


def auto_write_to_file(filepath: str, dir):
    with open(filepath, "w") as file:
        for x in range(0, len(os.listdir(dir))):
            if x % round(len(os.listdir(dir)) / 100) == 0:
                print(str(int(x / round(len(os.listdir(dir)) / 100))) + "% done with writing to CSV file")
            file.write("{}\n".format(0))


# full audio file name with extension
audio_files = []

for audio in audio_files:
    filler = 1   # Initial value of first frame
    audio_file = audio_files[audio]

    #Inital Variables
    folder = audio_file[:-4] + ' Folder'
    dir = path + folder  # Folder with frames of audio we're pulling from

    automatic_manual = int(input("Enter 0 to automatically score with all 0s and 1 to manually score: "))

    #Output file of scores
    data_scores = audio_file[:-4] + " Data.csv"

    if automatic_manual == 1:
        # Start of execution, allows for 3 seconds from starting this program to starting a audio to score.
        print("On your marks")
        time.sleep(1)
        print("Get Ready")
        time.sleep(1)
        print("Get Set")
        time.sleep(1)
        print("Go!")
        filler_tracker = record_data(dir, audio, filler)

        print("Done recording data, now writing to CSV")
        write_to_file(data_scores, filler_tracker)
    else:
        print("Now auto-scoring")
        auto_write_to_file(data_scores, dir)

    # reaction time fixer for the audio 
    # reaction_time_fixer(dst, 256, 144)

end_time = time.time()

print(end_time - init_time)
