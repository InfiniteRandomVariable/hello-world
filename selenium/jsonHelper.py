import json,io,random, common_classes
from json import dumps

class A(object):
	def __init__(self):
		self.b_list = []


#class B(object):
#	def __init__(self):
#		self.x = 'X'
#		self.y = random.random()

def encode_b(obj):
	if isinstance(obj, common_classes.Article):
		return obj.__dict__
	return obj

#url, title, numComments


#json.dumps(a, default=encode_b)
def writeToFile(timestamp,listObjects):
	if isinstance(listObjects,list) == False:
		raise Exception("Should be an article list")
	if isinstance(timestamp, int) == False:
		raise Exception("Should be a timestamp")

	a = A()
	a.b_list = listObjects
	fileName = '%s.json' % timestamp 
	with io.open(fileName, 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(a.__dict__, default=encode_b,encoding="utf-8",ensure_ascii=False,indent=1)))

#	print 'JSON: %s' % json.dumps(a.__dict__, default=encode_b,indent=1, ensure_ascii=False)

#theList = []
#for i in range(10):
#	theList.append(common_classes.Article('URL'))
#writeToFile(200, theList)

