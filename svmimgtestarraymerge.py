
import cv2
import numpy as np
from matplotlib import pyplot as plt
from hog import Hog_descriptor
import os

svm_params = dict( kernal_type = cv2.SVM_POLY,
					svm_type = cv2.SVM_C_SVC,
					C = 2.67, gamma = 5)
SZ = 20
bin_n = 16
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR
inversehash ={}



def readimages(root,attribute):
	folderpaths = os.listdir(root)

	labels = []
	for line in open(attribute):
		labels.append(line)

	allfortrain = {}
	# for folder in folderpaths:
	# folderpath = os.path.join(root,folder)
	# 	if os.path.isdir(folderpath) == 0:
	# 		continue
	trainingimages = []
	images = os.listdir(root)

	cnt = 0
	for image in images:
		print 'training ' + str(cnt) + ' image'
		label = labels[cnt]
		# print "image",image
		fullfilename=os.path.join(root,image)
		# results = my_ocr(fullfilename)
		img = cv2.imread(fullfilename, cv2.IMREAD_GRAYSCALE)
		# for result in results:
		# 	leftup = result['vertexes_location'][3]
		# 	rightdown = result['vertexes_location'][1]
		# 	pt1 = (leftup['x'],leftup['y'])
		# 	pt2 = (rightdown['x'],rightdown['y'])
		# 	color = np.int0((img[pt1[1],pt1[0]]+img[pt2[1],pt2[0]])/2)
		# 	cv2.rectangle(img, pt1, pt2, color,-1)
		if img is not None:
			size = max(img.shape[0],img.shape[1])
			img = cv2.resize(img, (size,size))
			size = int(size/2)
			hog = Hog_descriptor(img, cell_size=size, bin_size=16)
			vector, img = hog.extract()
			#print "lenin",len(vector)
			vector = vector[0]
			#print "lenin",len(vector)
			trainingimages.append(vector)
				# plt.imshow(img,cmap=plt.cm.gray)
				# plt.show()
			allfortrain[label] = trainingimages
		cnt += 1
	return allfortrain

def getreflect(f):
	for line in open(f):
		labelhash,label = line.split('\t')
		inversehash[labelhash] = label

	  
def trainsvm(materials):
	svm = cv2.SVM()
	responses = []
	trainData = []
	labels = open('label.txt','a')
	for label, vectors in materials.items():
		labelhash = hash(label) % 1000000

		labels.write(str(labelhash)+'\t'+str(label))

		#inversehash[labelhash] = label
		charact = np.float32(vectors).reshape(-1,64)
		for cha in charact:
			trainData.append(cha)
		for i in range(len(vectors)):
			responses.append(labelhash)

	trainData = np.array(trainData)
	# print "out",trainData
	responses = np.float32((np.array(responses))[:,np.newaxis])
	# print "reout",responses
	# responses =  np.float32((responses)[:,np.newaxis] )
	# print "responses",responses
	svm.train(trainData, responses, params = svm_params)
	svm.save('svm_image.dat')
	return svm

def getsvm(data):
	svmmodel = cv2.SVM()
	svmmodel.load(data)
	return svmmodel

def testsvm(svm, root):
	images = os.listdir(root)
	testimages = []
	for image in images:
		print image ,"image"
		fullfilename = os.path.join(root,image)
		img = cv2.imread(fullfilename, cv2.IMREAD_GRAYSCALE)
		size = max(img.shape[0],img.shape[1])
		img = cv2.resize(img, (size,size))
		size = int(img.shape[0]/2)
		hog = Hog_descriptor(img, cell_size=size, bin_size=16)
		vector, img = hog.extract()
		# vector = np.float32(np.array(vector))
		testimages.append(vector[0])
	testimages = np.float32(np.array(testimages))
	result = svm.predict_all(testimages)
	return result



# trainsvm(readimages('materials'))
#trainsvm(readimages('materials'))
# getsvm('svm_image.dat')
# exit()

# fullfilename = 'a002.jpg'
# img = cv2.imread(fullfilename, cv2.IMREAD_GRAYSCALE)

trainsvm(readimages('materials','names.txt'))
# trainsvm(readimages('materials2','name.txt'))
# svmmodel = getsvm('svm_image.dat')
# getreflect('label.txt')
# #result = testsvm(trainsvm(readimages('materials')), 'test').ravel()
# result = testsvm(svmmodel,'test').ravel()
# for i in result:
# 	print inversehash[str(int(i))]
# exit()

