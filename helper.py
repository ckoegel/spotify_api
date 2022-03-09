import math

def parse_time(time_ms) :   # parses a time duration in ms into a h:m:s string
    time_s = time_ms / 1000
    time_min = time_s / 60
    time_sec = time_s % 60
    
    if time_s > 3599 :
        time_hour = time_s / 3600
        time_min = time_s % 3600 / 60
        time_min_sec = str(math.trunc(time_hour)) + ":" + "{0:0>2}".format(str(math.trunc(time_min))) + ":" + "{0:0>2}".format(str(round(time_sec)))
    else :
        time_min_sec = str(math.trunc(time_min)) + ":" + "{0:0>2}".format(str(round(time_sec)))
    
    return time_min_sec