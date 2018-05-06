'''
Shijn Hou sh3658@columbia.edu
A multi-threaded script that scrapes images in three categories
download them to corresponding folder
'''
import csv
import logging
import sys
import threading
from threading import Condition

import pexpect

logging.basicConfig(level=logging.DEBUG,
	format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

cv = Condition()
N = 10
wait = 0
flag = False

r = '../data/recyclable.csv'
c = '../data/compost.csv'
s = '../data/special.csv'
t = '../data/trash.csv'
path = "/Users/shijun/Desktop/ican-project/recognition/utils/scrapeImages.py"
rdir = "../img/recycle"
cdir = "../img/compostable"
sdir = "../img/special"
tdir = "../img/trash"

with open(r, 'r') as f:
    data = csv.reader(f)
    rec = list(data)[0]
with open(c, 'r') as f:
    data = csv.reader(f)
    compost = list(data)[0]
with open(s, 'r') as f:
    data = csv.reader(f)
    special = list(data)[0]
with open(t, 'r') as f:
	data = csv.reader(f)
	trash = [a[0] for a in list(data)]

def imgDownload(imgDir, data):
	'''
	Scrape images in three categories, multi-threaded
	:imgDir: str(): path to which the images are downloaded
	:data: List[]: shared data source
	'''
	# synchronization
	global wait
	global flag
	logging.debug('Starting')
	while True:
		cv.acquire()
		if flag:
			logging.debug('KeyboardInterrupt, exiting...')
			return
		while not data:
			wait += 1
			if wait == 4 * N:
				cv.notify()
				cv.release()
				logging.debug('Exiting...')
				return
			cv.wait()
			wait -= 1
		item = data.pop()
		logging.debug('{0} to go'.format(len(data)))
		if data:
			cv.notifyAll()
		cv.release()
		# download images
		command = "python " + path + " --search " + item + " --num_images 30" + " --directory " + imgDir
		worker = pexpect.spawn(command)
		worker.expect([pexpect.EOF, pexpect.TIMEOUT])

if __name__ == "__main__":
	print 'Start image crawler'
	for i in range(N):
		t = threading.Thread(target=imgDownload, args=(cdir, compost))
		t.start()
	for i in range(N):
		t = threading.Thread(target=imgDownload, args=(rdir, rec))
		t.start()
	for i in range(N):
		t = threading.Thread(target=imgDownload, args=(sdir, special))
		t.start()
	for i in range(N):
		t = threading.Thread(target=imgDownload, args=(tdir, trash))
		t.start()
	while True:
		try:
			pass
		except KeyboardInterrupt:
			flag = True
			print 'Crawler exit...'
			sys.exit
