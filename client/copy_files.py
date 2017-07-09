import os

print 'running copy_files script...'

path = '/home/pi/pi-spy-files/videos'

for filename in os.listdir(path):
    # do your stuff
    print 'file name: ' + filename
