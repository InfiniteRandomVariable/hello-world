from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import common_classes, jsonHelper, timeHelper,re,time
import pytz, datetime
import calendar
import re
import randomTime
import sys


##PROBLEM
## only can find the first 4 items. Maybe memory problem?


def timeToTimeStamp(timeStr):
	
	timeZONE = 'US/Eastern'

	##2014-12-22
	local = pytz.timezone (timeZONE)
	naive = datetime.datetime.strptime (timeStr, "%Y-%m-%d")
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone (pytz.utc)
	timeStamp = calendar.timegm(utc_dt.utctimetuple())
	#print timeStamp
	return timeStamp



browser = webdriver.Firefox()

NAME='nytimes' 
BASE= 'http://www.%s.com' % NAME 

WEBSITE_URL = '%s' % BASE

#browser.get(WEBSITE_URL)
#browser.get('http://www.nytimes.com/most-popular')
browser.get('https://myaccount.nytimes.com/auth/login?URI=http://www.nytimes.com/most-popular')

rowElements = []
divider = 3
MIN_LIKES = 30/divider
MIN_COMMENT_NUM = 100/divider
MAX_PAGE_VISIT = 3
WORDS_LIMIT = 140
MAX_RANKING=5
WAIT_SECONDS = 3

POPULARS = '//ol/li/a'
SEARCH_START = 10
SEARCH_END = 18





#id input#userid
#id input#password
# button#js-login-submit-button

#step 1
#log-in


#.button.login-button.login-modal-trigger
#input#login-password
#input#login-email
#button#login-send-button

time.sleep(randomTime.randomTime(5))
pages=[]

try:
	print "1"
	#WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.button.login-button'))).click()
	print "2"
	WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input#userid'))).send_keys('lauyukpui@yahoo.com')
	print "3"
	time.sleep(randomTime.randomTime(3))
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input#password'))).send_keys('NYTIMES2014')
	print "4"
	time.sleep(randomTime.randomTime(5))
	print "KILL process"
	WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#js-login-submit-button'))).click()

except Exception as e:
	print "LOGIN Exception: %s" % e

# sys.exit()

#//ol/li/a
#//ol/li/a[@href]

try:
	print "11"

	
	popularElms = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH,POPULARS)))[SEARCH_START:SEARCH_END]

	for pE in popularElms[:]:
		print "12"
		_url = pE.get_attribute('href')
		url = re.sub(r'\?src=mv',"",_url)
		print "13"
		if 'interactive' in url:
			print "BLOCKED URL: %s" % url
			continue
		a = common_classes.Article(url)
		a.title = pE.text.strip()

		print "Title: %s" % a.title
		if len(a.title) < 4:
			continue

		urlWithoutArticleLink = re.sub(r'\/?[\=\?\w\.\-]+$',"",a.url)
		print "URL: %s" % a.url
		a.tag = re.search(r'[\w]+$', urlWithoutArticleLink).group()
		print "TAG: %s" % a.tag
		pages.append(a)
	

except Exception as e:
	print "LOGIN Exception: %s" % e

#https://myaccount.nytimes.com/auth/login?URI=http://www.nytimes.com/most-popular

isFirstPage = True
	#print "6"
for article in pages[:]:

	browser.get(article.url)
	if isFirstPage == False:
		time.sleep(WAIT_SECONDS)
	isFirstPage = False
	try:
		commentButton = WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.button.comments-button.theme-kicker')))
	except Exception as e:
		print "Exception commentButton: %s" % e
		continue

	numCommentText = commentButton.find_element_by_css_selector('.count').text.strip()
	print "numComments: %s" % numCommentText
	try:
		article.numComments = int(numCommentText)
	except Exception as e:
	 	article.numComments = 1
	 	print "Exception numComments: %s" % e

	commentButton.click()


	time.sleep(WAIT_SECONDS)
	WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.tab.reader'))).click()
	time.sleep(WAIT_SECONDS*2)
	article.topComment = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.comment-text'))).text.strip()[0:WORDS_LIMIT]
	if len(article.topComment) > (WORDS_LIMIT -2):
		article.topComment = "%s..." % article.topComment
	print "topComment %s" % article.topComment
	article.topCommentNum = int(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.recommend-count'))).text.strip())
	print "topCommentNum %s" % article.topCommentNum
	timeText = str(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.dateline'))).get_attribute('datetime'))
	print "timeText %s" % timeText

	article.age = int(timeToTimeStamp(timeText))/1000
	print "article.age %s" % article.age	

#article.tag = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,".blogName>a"))).text.strip()

	if len(article.title) > 2 and len(article.topComment) > 2 and len(article.url) > len(BASE) and article.age > 10 and article.topCommentNum > MIN_LIKES:
		rowElements.append(article)
	else:
		print "article title %s \narticle.topComment %s \narticle.url %s \narticle.age %s article.topCommentNum %s " %( article.title,article.topComment, article.url, article.age, article.topCommentNum)
		pass
		
jsonHelper.writeToFile(timeHelper.APP_TIMESTAMP(),rowElements,NAME)
browser.quit()