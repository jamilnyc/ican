'''
Shijun Hou sh3658@columbia.edu
A multi-threaded script that
1. Run rekognition on those images
2. Label the results as they are.
	1: recycle, 2: compostable, 4: special, 8: trash
3. Generate the final train data file
'''
import os
import sys
import threading
from threading import Condition, Lock

import rek

#logging.basicConfig(level=logging.DEBUG,
#                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
#                    )

cv = Condition()
lock = Lock()
N = 10
wait = 0
flag = False

rdir = "../img/recycle"
cdir = "../img/compostable"
sdir = "../img/special"
tdir = "../img/trash"
target = "../data/trainData.csv"

def worker(imgPool, label):
	'''
	:imgPool: List[] of image paths
	:label: str()
	'''
	global wait
	global flag
	#logging.debug('Worker start')
	while True:
		if flag:
			#logging.debug('KeyboardInterrupt')
			return
		cv.acquire()
		while not imgPool:
			wait += 1
			if wait == 3 * N:
				cv.notifyAll()
				cv.release()
				# logging.debug('Worker Exit...')
				return
			cv.wait()
			wait -= 1
		img = imgPool.pop()
		#logging.debug('{0} to go'.format(len(imgPool)))
		if imgPool:
			cv.notifyAll()
		cv.release()
		# Rekognition
		txt = rek.imageRec(img)
		lock.acquire()
		rek.appendToCsvFile(target, [txt, label])
		lock.release()

def singleWorker(imgPool, label):
	for img in imgPool:
		txt = rek.imageRec(img)
		rek.appendToCsvFile(target, [txt, label])

def readImg():
	'''
	Get three lists of image paths
	:rtype: List[], List[], List[]
	'''
	rImg = [f for f in os.listdir(rdir) if os.path.isfile(os.path.join(rdir, f))]
	cImg = [f for f in os.listdir(cdir) if os.path.isfile(os.path.join(cdir, f))]
	sImg = [f for f in os.listdir(sdir) if os.path.isfile(os.path.join(sdir, f))]
	tImg = [f for f in os.listdir(tdir) if os.path.isfile(os.path.join(tdir, f))]
	for i in range(len(rImg)):
		rImg[i] = '../img/recycle/' + rImg[i]
	for i in range(len(cImg)):
		cImg[i] = '../img/compostable/' + cImg[i]
	for i in range(len(sImg)):
		sImg[i] = '../img/special/' + sImg[i]
	for i in range(len(tImg)):
		tImg[i] = '../img/trash/' + tImg[i]
	return rImg, cImg, sImg, tImg


if __name__ == '__main__':
	print 'Start generating training data'
	rImg, cImg, sImg, tImg = readImg()
	'''
	try:
		singleWorker(rImg, '1')
		singleWorker(cImg, '2')
		singleWorker(sImg, '4')
	except KeyboardInterrupt:
		flag = True
		print 'Exit...'
		sys.exit
	'''
	for i in range(N):
		t = threading.Thread(target=worker, args=(cImg, '2'))
		t.start()
	for i in range(N):
		t = threading.Thread(target=worker, args=(sImg, '4'))
		t.start()
	for i in range(N):
		t = threading.Thread(target=worker, args=(tImg, '8'))
		t.start()
	while True:
		try:
			pass
		except KeyboardInterrupt:
			flag = True
			print "genData exit..."
			sys.exit
