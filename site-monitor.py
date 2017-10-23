import datetime
import httplib
import urllib2
import requests
import time
import json
import urllib2
import sys


file = open("site-monitor.config", "r")
sites = file.readline().split(',')  # a comma-delimited string for the name of sites to monitor, in the form of: SiteFoo, SiteBar
print "sites: ", sites
urls = file.readline().split(',') # a comma-delimited string for the url's of sites to monitor, the the form of: https://foo.com, https://bar.com
print "urls: ", urls
webHook = file.readline() # a webhook address to send notification messages, in the form of: https://hook.app.com/blahblah
print "webhook: ", webHook

monitor_sleep = 15
issue_sleep = 5

def get_status(url):
	try:
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		return response.getcode()
		response.close()
	except urllib2.URLError, e:
		print e
	except urllib2.HTTPError, e:
		print e
	except httplib.HTTPException, e:
		print e
	except Exception:
		print "Generic error"
		
def get_sites_with_issues():
	result = []
	for i in range(len(sites)):
		url = urls[i]
		status = get_status(url)
		if( status < 200 or status >= 400):
			result.append(sites[i] + " :no-signal:")
	return result
		
def notity(messages):
	result = []
	print "Sending notification ..."
	for i in range(len(messages)):
		try:
			time = datetime.datetime.utcnow().strftime("%H:%M:%SZ")
			utcnow = datetime.datetime.utcnow()
			data = {'text': str(time) + ' - ' + messages[i]}
			req = urllib2.Request(webHook)
			req.add_header('Content-Type', 'application/json')
			response = urllib2.urlopen(req, json.dumps(data))
			response.close()
		except Exception, e:
			print "Could not notify"
			print e
		
	


last_issues = []
while 1:
	issues = get_sites_with_issues()
	
	if( len(issues) > 0 ):
		print "Detected issues: ", issues
		if( len(last_issues) == 0 ):  # was issue-free before this point
			time.sleep(issue_sleep)
			issues = get_sites_with_issues()
			#only send notification when it's a fresh issue
			if( len(issues) > 0 ):
				print "Persisted issue state:", issues
				notity(issues)
			else:
				print "Recovered"
	else:			
		if( len(last_issues) > 0 ):
			notity(['Services are back :sunny:'])
			print "Back to normal"	
		else:
			print "Normal"	
			
	last_issues = issues	
	time.sleep(monitor_sleep)		
	
			
		
