#!/usr/bin/env python

# pyNexpose is a python module that interfaces with the Rapid 7 Nexpose API versions 1.1 and 1.2
# Depends on the Elementtree python module easy_install elementtree

import urllib2
import os, os.path
import elementtree.ElementTree as ET

# dump the HTTP requests to debug issues further
#urllib2.install_opener(urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=10)))

# your API endpoint defined here
uri = 'https://x.x.x.x/api/1.1/xml'

# your API credentials defined here
nx_user = 'user'
nx_passwd = 'pass'

def apireq(postdata):
	headers = {"Content-type" : "text/xml"}
	try:
		req = urllib2.Request(uri, postdata, headers)
		res = urllib2.urlopen(req).read()
		resxml = ET.fromstring(res)
		success = resxml.attrib.get('success')
		if success != '0':
			return res
		else:
			return 'Error: ' + resxml[0][0][0].text
	except Exception as e:
		raise Exception("The Transform has returned: %s" % e)

def checkdir(path):
	if os.path.exists(path):
		pass
	else:
		os.makedirs(path)

# Login function that returns a session ID to authenticate all other requests
def nexlogin():
	headers = {"Content-type" : "text/xml"}
	post_data = "<LoginRequest user-id=\"" + nx_user + "\" password=\"" + nx_passwd + "\" />"
	try:
		req = urllib2.Request(uri, post_data, headers)
		res = urllib2.urlopen(req).read()
		resxml = ET.fromstring(res)
		success = resxml.attrib.get('success')
		if success != '0':
			return resxml.attrib.get('session-id')
		else:
			return 'Error: ' + resxml[0][0][0].text
	except Exception as e:
		raise Exception("The Transform has returned: %s" % e)

# Logout function to terminate a session
def nexlogout(session):
	headers = {"Content-type" : "text/xml"}
	post_data = "<LogoutRequest session-id=\"%s\" />" % session
	try:
		req = urllib2.Request(uri, post_data, headers)
		res = urllib2.urlopen(req).read()
		resxml = ET.fromstring(res)
		success = resxml.attrib.get('success')
		if success != '0':
			pass
		else:
			return 'Error: ' + resxml[0][0][0].text
	except Exception as e:
		raise Exception("The Transform has returned: %s" % e)

# Site Management Functions
# Function to list all sites
def sitelisting(session):
	postdata = "<SiteListingRequest session-id=\"%s\"></SiteListingRequest>" % session
	return apireq(postdata)

# Function to view the site configuration of a specified site
def siteconfig(session, siteid):
	postdata = "<SiteConfigRequest session-id=\"%s\" site-id=\"%s\"></SiteConfigRequest>" % (session, siteid)
	return apireq(postdata)

# TODO Create a site for a host and start a scan
def host_site(siteid, sitename, description, hosts, engineid):
	#site = """<Site id=\"-1\" name=\"%s\"><Hosts>%s</Hosts><ScanConfig configID=\"1\" name=\"Full Audit\" templateID=\"full-audit\" configVersion=\"3\" /></Site>""" % (sitename, hosts)
	site = """<Site id=\"%s\" name=\"%s\" description=\"%s\"><Hosts>%s</Hosts><ScanConfig configID=\"1\" name=\"Full Audit\" templateID=\"full-audit\" engineID=\"%s\" configVersion=\"3\" /></Site>""" % ( siteid, sitename, description, hosts, engineid )
	return site

# Function to save a new site
def sitesave(session, site):
	postdata = "<SiteSaveRequest session-id=\"%s\" >%s</SiteSaveRequest>" % (session, site)
	return apireq(postdata)

# Function to list all devices within a site as well as their risk rating
def sitedevicelisting(session, siteid):
	postdata = "<SiteDeviceListingRequest session-id=\"%s\" site-id=\"%s\"></SiteDeviceListingRequest>" % (session, siteid)
	return apireq(postdata)

# Function to view the scan hostory of a specified site
def sitescanhistory(session, siteid):
	postdata = "<SiteScanHistoryRequest session-id=\"%s\" site-id=\"%s\"></SiteScanHistoryRequest>" % (session, siteid)
	return apireq(postdata)

# Scan Management Functions
# Function to scan a specified site
def sitescan(session, siteid):
	postdata = "<SiteScanRequest session-id=\"%s\" site-id=\"%s\"></SiteScanRequest>" % (session, siteid)
	return apireq(postdata)

# TODO SiteDevicesScanRequest function See API 1.1 docs

# List all scan activity across all scan engines
def scanactivity(session):
	postdata = "<ScanActivityRequest session-id=\"%s\"></ScanActivityRequest>" % (session)
	return apireq(postdata)

# List the status of a scan
def scanstatus(session, scanid):
	postdata = "<ScanStatusRequest session-id=\"%s\" scan-id=\"%s\"></ScanStatusRequest>" % (session, scanid)
	return apireq(postdata)

# Lists statistics of a scan
def scanstatistics(session, scanid):
	postdata = "<ScanStatisticsRequest session-id=\"%s\" scan-id=\"%s\"></ScanStatisticsRequest>" % (session, scanid)
	return apireq(postdata)

# Asset group listing 
def assetgrouplisting(session):
	postdata = "<AssetGroupListingRequest session-id=\"%s\"></AssetGroupListingRequest>" % (session)
	return apireq(postdata)

# Vulnerability listing 
def vulnlisting(session):
	postdata = "<VulnerabilityListingRequest session-id=\"%s\"></VulnerabilityListingRequest>" % (session)
	return apireq(postdata)

# report template listing
def reporttemplist(session):
	postdata = "<ReportTemplateListingRequest session-id=\"%s\" />" % (session)
	return apireq(postdata)

# Generate an ad-hoc vulnerability report of the last scan
def adhoc_report(session, siteid):
	headers = {"Content-type" : "text/xml"}
	xml1 = "<ReportAdhocGenerateRequest session-id=\"%s\">\n" % session
	xml2 = "<AdhocReportConfig template-id=\"audit-report\" format=\"raw-xml-v2\">\n"
	xml3 = "<Filters>\n"
	xml4 = "<filter type=\"site\" id=\"%s\" />\n" % siteid
	xml5 = "<filter type=\"vuln-status\" id=\"vulnerable-version\" />\n"
	xml6 = "</Filters>\n"
	xml7 = "</AdhocReportConfig>\n"
	xml8 = "</ReportAdhocGenerateRequest>"
	postdata = xml1 + xml2 + xml3 + xml4 + xml5 + xml6 + xml7 + xml8
	try:
		req = urllib2.Request(uri, postdata, headers)
		res = urllib2.urlopen(req)
		return res
	except SyntaxError as e:
		return 'Something went wrong: %s' % e
