#!/usr/bin/env python
#
#
# Create scans from target list using NeXpose API
#
# Born from Nextego (https://github.com/bostonlink/Nextego)
#
#
# @gitrc 2014
#
#

import datetime
import time
import os,sys
from pyNexpose import *

try:
        siteid = int(sys.argv[1])
except:
        print 'usage: ' + sys.argv[0] + ' <site id>'
        sys.exit(1)

response = []

filename = '/tmp/targets.txt'
lines = [line.strip() for line in open(filename)]

targets = ''
for line in lines:
	#targets += '<host>' + line + '</host>'
        targets += '<range from=\"' + line + '\" to=\"\"/>'

# Nespose API session login
session = nexlogin()

# Nexpose site creation
config = siteconfig(session, siteid)
resxml = ET.fromstring(config)
#print(resxml.findall('.//*'))
sitename = resxml.find('./Site').attrib['name']
description = resxml.find('./Site').attrib['description']
engineid = resxml.find('./*/ScanConfig').attrib['engineID']
newsite = host_site(siteid, sitename, description, targets, engineid)
nexsite = sitesave(session, newsite)
resxml = ET.fromstring(nexsite)
siteid = resxml.attrib.get('site-id')

if resxml.attrib.get('success') == '1':
    # Nexpose Scan Site
    launchscan = sitescan(session, siteid)
    launchres = ET.fromstring(launchscan)
    if launchres.attrib.get('success') == '1':
        for child in launchres:
            scanid = child.attrib.get('scan-id')
            status = scanstatus(session, scanid)
            statusxml = ET.fromstring(status)
	# have to comment out the below because of duration... 
        #    while statusxml.attrib.get('status') == 'running':
        #        time.sleep(5)
        #        status = scanstatus(session, scanid)
        #        statusxml = ET.fromstring(status)
        #        continue
            response = 'Scan Submitted: ' 'sitename=' + sitename + ' siteid=' + siteid + ' scanid=' + scanid + ' status=' + statusxml.attrib.get('status')
	print response
nexlogout(session)
