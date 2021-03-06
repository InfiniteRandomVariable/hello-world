from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os, re, jsonHelper
import os.path
import time
from time import mktime
import datetime



#ABS_PATH = '~/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium'
CRED = '.s3'
ACCESS = 'accesskey'
SECRET = 'secret'
BUCKET_NAME = 'data.hotoppy.com'
IMAGE_PATH = '/imaging/images'
SECONDS_IN_A_DAY = 24 * 60 * 60
OneAndHalfDay = SECONDS_IN_A_DAY * 2
#OneAndHalfDay = 1
UPLOAD_SUFFIX = 'uploaded'
#IMAGE_KEY_SUBFOLDER = "images/"
IMAGE_KEY_SUBFOLDER = "i/"
MAX_IMAGE_SIZE = 60000
MIN_IMAGE_SIZE = 5000
#TEMP_PATH = 'guardian/1420592.json'

def absoluteImagePath():
	return "{0}{1}".format(jsonHelper.getCompleteFilePath(), imagePath())

def imagePath():
	return IMAGE_PATH

def readCred():
	if len(CRED) < 1:
		#print "please provide the credential file name"
		return 
	counter = 0
	cred_path = jsonHelper.getCompleteFilePath(CRED)
	dictCred = { ACCESS: '' , SECRET: '' }
	with open(cred_path) as f:
		content = f.read().splitlines()
		dictCred[ACCESS] = content[counter]
		counter = counter + 1
		dictCred[SECRET] = content[counter]
		#print content
		return dictCred

def accessBucket(buckName=None):

	if not buckName or len(buckName) < 1:
		buckName = BUCKET_NAME
		#return

	try:
		cred = readCred()
		conn = S3Connection(cred[ACCESS], cred[SECRET])
		b = None
		try:
			b = conn.get_bucket(buckName)
		except Exception as e:
			b = conn.create_bucket(buckName)

		if not b:
			print("Error: bucket cannot be nil")
			return
		else:
			return b

	except Exception as e:
		print("Access Bucket Error: {0}".format(e))

def getBucketList(pathToFileName=IMAGE_KEY_SUBFOLDER, bucket=None):

	if not bucket:
		bucket = accessBucket()

	#nameList = [v.name[len(pathToFileName):] for v in list(b.list(pathToFileName, "/"))]
	return list(bucket.list(pathToFileName, "/"))

def getBuckNameList(pathToFileName=IMAGE_KEY_SUBFOLDER, bucket=None):
	keyList = getBucketList(bucket=bucket)

	return [v.name for v in keyList]


def deleteProcedure(specifiedDuration=OneAndHalfDay):

	dt = datetime.datetime.now()
	print("1")
	nowInSeconds = time.mktime(dt.timetuple())
	b = accessBucket()
	keyList = getBuckNameList(bucket=b)

	for keyName in keyList[:]:
		
		imagekey = b.get_key(keyName)
		print("Not Uploading file name: {0} last-modified: {1}".format(keyName, imagekey.last_modified))
		##"Thu Jan 29 19:13:17 GMT-800 2015"

		# print("imageNameList: {0}".format(imageNameList[0]))

		#2015-02-19T18:32:32.000Z

		modified = time.strptime(imagekey.last_modified, '%a, %d %b %Y %H:%M:%S %Z')

		#convert to datetime
		print("time date 0 keyName: {0}".format(keyName))
		mdt = datetime.datetime.fromtimestamp(mktime(modified))
		print("time date 1")
		#(dt.datetime(1970,1,1)).total_seconds()
		
		#modifiedTimeInSeconds = mdt.datetime(1970,1,1).total_seconds()
		modifiedTimeInSeconds = time.mktime(mdt.timetuple())
		print("time date 2")

		durationInSeconds = nowInSeconds - modifiedTimeInSeconds
		#systemPath = jsonHelper.getCompleteFilePath()
		#print("should delete: {0}{1}/{2}".format(systemPath, dirname[1:], name))
		#os.remove(localPath)
		#assume default dirname is "./xyz"
		#deleteFilePath = "{0}{1}/{2}".format(systemPath, dirname[1:], name)

		if durationInSeconds > specifiedDuration:
			try:
				print("LONGER THAN ONE DAY deleting {0}".format(imagekey))
				b.delete_key(imagekey)
		#		os.remove(deleteFilePath)
			except Exception as e:
				print ("Exception in deleting key: {0} - {1}".format(imagekey, e))

		else:
			print("WITHIN ONE DAY {0}".format(imagekey))





#NOTE: the S3 path will be lower case where local file name maybe upper case
#Parameters: forwardWrite default to 5 to ensure continuity of the data for upcoming event and expected the newer data will overwrite this
#			  localPath, consist of this pattern publicationName/timestamp.json
#			
# minor error [Errno 1] Operation not permitted: '/Users/pro001/Desktop/Dev/Learning/tests/scrapWeb/hello-world/selenium/imaging/images'
# possible fix: http://stackoverflow.com/questions/10937806/oserror-error-1-operation-not-permitted
# chown -R username:groupname .

def sendData( localPath, buckName=None, forwardWrite=36):
	
	#thelocalPath = "{0}".format( localpath )
	##print "localPath 1 %s" % localPath

	

	if not buckName or len(buckName) < 1:
		buckName = BUCKET_NAME
		#return

	if len (localPath) < 1:
		return


	try:
		# cred = readCred()
		# conn = S3Connection(cred[ACCESS], cred[SECRET])
		b = accessBucket()
		# try:
		# 	b = conn.get_bucket(buckName)
		# except Exception as e:
		# 	b = conn.create_bucket(buckName)

		# if not b:
		# 	#print "Error: bucket cannot be nil"
		# 	return

		systemPath = jsonHelper.getCompleteFilePath().lower().split('/')
		localPathArray = localPath.lower().split('/')
		print("systemPath: {0}, localPath: {1}".format(systemPath, localPathArray))

		for pathIndex in range(len(systemPath)):
			pathStr = systemPath[pathIndex]
			if pathStr.find(localPathArray[pathIndex]) < 0:
				print("NOT MATCH Path name s3Interface: {0}".format(localPathArray[pathIndex]))
				return


		#re.sub(r'\.json$',"",localPath.lower())
		#strippedPath = re.sub(r'\.json$',"",localPath.lower())



		
		if len(localPath) < 7 or len(localPathArray) < 2:
			print("Error check localpath {0}".format(localpath))
			return;


		if IMAGE_PATH in localPath:
		 	##image Operation

		 	topdir = '{0}'.format(localPath)
		# 	# The arg argument for walk, and subsequently ext for step
			exten = '.jpg'
			#imageNameList = [v.name[len("images/"):] for v in list(b.list("images/", "/"))]
			imageNameList = [v.name[len(IMAGE_KEY_SUBFOLDER):] for v in list(b.list(IMAGE_KEY_SUBFOLDER, "/"))]
			# print("imageName: {0}".format(imageNameList[4]) )

			uploadSuffixSubstringHelper = -len(UPLOAD_SUFFIX)

			##PRECONDITION
			## it download image files to a local folder in python
			## on the bash level, the images should be reformatted within the range of acceptable bytes size as JPG images and JPG extension
			##
			##CONDITION 
			## it will iterate through the destination folders.
			## searches for jpg files to upload and compare the S3 image folder.
			##    IF no match is identified and conform to acceptable size, it will be uploaded to the S3 folder and rename the extension to uploaded.
			##    elif match is identified with jpg extension"
			## 			delete the file in the local machine
			## 	  elif file match uploaded extension
			##			check if exceeded the minimum time
			##				delete the file in the S3 and local machine
			##			else do nothing
			##
			##
			##
			## 

			def step(ext, dirname, names):
				#global _localPath

				ext = ext.lower()
				print("0 ext: {0}".format(ext))
				dt = datetime.datetime.now()
				print("1")
				nowInSeconds = time.mktime(dt.timetuple())

				print("2")

				for name in names[:]:

					if len(name) <2:
						continue

					#nameInTheList will be used for idenitfying whether the name is in the S3 data network.
					nameInTheList = False
					_name =""
					if name.lower().endswith(UPLOAD_SUFFIX) is True:
						_name = name[:uploadSuffixSubstringHelper]
					else:
						_name = name

					# check the image name exists in the cloud for with or without upload suffix
					# this will double check if the image has been uploaded to the cloud as sometime the image fail to upload but is incorrectly rename to upload suffix.

					if _name in imageNameList[:]:
						nameInTheList = True
					else:
						nameInTheList = False


					
					#print("name[:-len(UPLOAD_SUFFIX)]: {0}".format(name[:-(len(UPLOAD_SUFFIX)]))
					print("3 try: {0}".format(name[:uploadSuffixSubstringHelper]))


					if name.lower().endswith(ext) is True and not nameInTheList or name.lower().endswith(UPLOAD_SUFFIX) is True and not nameInTheList:

						if name.lower().endswith(UPLOAD_SUFFIX) is True:
							thisName = name[:uploadSuffixSubstringHelper]
						else:
							thisName = name

						
						print("4")

						keyName = "{0}{1}".format(IMAGE_KEY_SUBFOLDER, thisName)

						print("2 keyName: {0}".format(keyName))
						imagekey = b.new_key(keyName)

						print("Uploading file name: {0}".format(thisName))

						imagekey.Content_Type = "image/jpeg"

						try:
							pathToImageFile = "{0}/{1}".format(localPath,name)
							img_size = os.stat(pathToImageFile).st_size
							if img_size > MAX_IMAGE_SIZE or MIN_IMAGE_SIZE > img_size:
								print(" WARNING: improper image size {0}: {1}".format(img_size, name ))
								os.remove(pathToImageFile)
								continue

							imagekey.set_contents_from_filename(pathToImageFile)
							imagekey.make_public()

							if name.lower().endswith(ext) is True:
								localPathExt = "{0}{1}".format(pathToImageFile, UPLOAD_SUFFIX)
								os.rename(pathToImageFile, localPathExt)

							#if os.path.exists(pathToImageFile):
							#	os.remove(pathToImageFile)

						except Exception as e:
							print("Exception uploading image 0: {0} - {1}".format(name, e))

					elif name.lower().endswith(UPLOAD_SUFFIX) is True and nameInTheList or name.lower().endswith(ext) is True and nameInTheList:

						if name.lower().endswith(UPLOAD_SUFFIX) is True:
							_name = name[:uploadSuffixSubstringHelper]
						else:
							_name = name

						keyName = "{0}{1}".format(IMAGE_KEY_SUBFOLDER, _name)
						imagekey = b.get_key(keyName)
						print("Not Uploading file name: {0} last-modified: {1}".format(keyName, imagekey.last_modified))
						##"Thu Jan 29 19:13:17 GMT-800 2015"

						# print("imageNameList: {0}".format(imageNameList[0]))

						modified = time.strptime(imagekey.last_modified, '%a, %d %b %Y %H:%M:%S %Z')

						#convert to datetime
						print("time date 0 keyName: {0}".format(keyName))
						mdt = datetime.datetime.fromtimestamp(mktime(modified))
						print("time date 1")
						#(dt.datetime(1970,1,1)).total_seconds()
						
						#modifiedTimeInSeconds = mdt.datetime(1970,1,1).total_seconds()
						modifiedTimeInSeconds = time.mktime(mdt.timetuple())
						print("time date 2")

						durationInSeconds = nowInSeconds - modifiedTimeInSeconds
						systemPath = jsonHelper.getCompleteFilePath()
						print("should delete: {0}{1}/{2}".format(systemPath, dirname[1:], name))
						#os.remove(localPath)
						#assume default dirname is "./xyz"
						deleteFilePath = "{0}{1}/{2}".format(systemPath, dirname[1:], name)

						if durationInSeconds > OneAndHalfDay and len(imageNameList) > 0:
							try:
								print("LONGER THAN ONE DAY deleting {0}".format(imagekey))
								b.delete_key(imagekey)
								os.remove(deleteFilePath)
							except Exception as e:
								print ("Exception in deleting key: {0} - {1}".format(imagekey, e))
						elif name.lower().endswith(ext) is True:
							pathToImageFile = "{0}/{1}".format(localPath,name)
							localPathExt = "{0}{1}".format(pathToImageFile, UPLOAD_SUFFIX)
							try:
								os.rename(pathToImageFile, localPathExt)
							except Exception as e:
								print ("Exception in deleting key: {0} - {1}".format(pathToImageFile, e))

						else:
							print("WITHIN ONE DAY {0}".format(imagekey))

					# elif name.lower().endswith(UPLOAD_SUFFIX) is True:
					# 	systemPath = jsonHelper.getCompleteFilePath()
					# 	deleteFilePath = "{0}{1}/{2}".format(systemPath, dirname[1:], name)
					# 	try:
					# 		print("Deleting Path: {0}".format(deleteFilePath))
					# 		os.remove(deleteFilePath)
					# 	except Exception as e:
					# 		print ("Exception in deleting path: {0} - {1}".format(deleteFilePath, e))


			os.path.walk(topdir, step, exten)


		else:

			##JSON Operation	
			
			timeName = localPathArray[len(localPathArray)-1]
			strippedPath = re.sub(r'\.json$',"",timeName.lower())
			timeStampStr = re.search( r'\d+$', strippedPath).group()
					
			timestamp = int(timeStampStr)	

			print 'strippedPath ' + strippedPath
			#publicationName = re.search( r'^\w+', strippedPath).group()

			publicationName = localPathArray[len(localPathArray)-2]
			print('publicationName {0}'.format(publicationName))
			if timestamp < 100 and len(publicationName) < 1:
				#print "error in publication name or time stamp"
				return

			# metaData = {'charset': 'utf-8', 'Content-Type': 'application/json; '}
			k = Key(b)
			# k.metadata = metaData
			k.Content_Type = 'application/json; charset=utf-8'
			k.content_disposition = 'inline'
			# k.content_encoding = 'gzip'

			for num in range(forwardWrite):

				if num == 0:

					k.key = "%s/%d.json" % (publicationName, timestamp)
					k.set_contents_from_filename(localPath)
					k.make_public()

				else:
					k.copy(buckName,"%s/%d.json" % (publicationName, timestamp)).make_public()

				
				timestamp = timestamp + 1
		#print("should delete: {0}".format(localpath))
		#os.remove(localPath)

	except Exception as e:
		print(e)
	#	print "ERROR s3Interface %s" % e

def uploadImagesProcedure():
	imagePath = jsonHelper.getCompleteFilePath('imaging', 'images')
	sendData(imagePath)

