import re


def truncatedStringForRow(text, WORD_LIMIT=250):
	if len(text) > (WORD_LIMIT -2):
		## tpC = re.sub(r'\.*$',"", text)
		return "%s..." % re.sub(r'\.+$',"", text.strip()[0:WORD_LIMIT])
	else:
		return text

def printArticle(art):
	try:
		print("Title: {0}".format(art.title))
		print("URL: {0}".format(art.url))
		print("NumComments: {}".format(art.numComments))
		print("TopComment: {0}".format(art.topComment))
		print("TopCommentNum: {}".format(art.topCommentNum))
		print("Age: {}".format(art.age))
		print("Tag: {0}".format(art.tag))
	except Exception as e:
		print("Print Exception: {0}".format(e))

#2 and art.numComments > 5 and len(art.url) > 2 and len(art.topComment) > 2 and art.topCommentNum

def checkArticle(art, minNumComments=2, minTopCommentNum=2):
	#integer = topCommentNum, age, numComments

	if art.title and art.img and art.topComment and art.url:
		print("article attribute exist {}".format(minTopCommentNum))
		if len(art.img) > 1 and len(art.title) > 2 and art.numComments > minNumComments and len(art.url) > 2 and len(art.topComment) > 2 and art.topCommentNum > minTopCommentNum and len(art.tag) > 1:
			return True
		else:
			return False
	else:
		print("article attribute not exist")
		return False
	  

