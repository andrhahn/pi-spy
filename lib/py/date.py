import datetime

print "Current date and time:"
print datetime.datetime.now().strftime("/home/pi/%Y-%m-%d_%H-%M-%S.h264")
