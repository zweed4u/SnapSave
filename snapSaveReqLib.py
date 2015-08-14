import os
import requests
from PIL import Image
import time
import errno
import subprocess
import threading


def timeout( p ):
	if p.poll() is None:
        	try:
        		p.kill()
        	        print '20 seconds are up! Error: process taking too long to complete--terminating'
       		except OSError as e: #race condition
                	if e.errno != errno.ESRCH:
                		raise


url='https://feelinsonice-hrd.appspot.com/bq/blob'
# 200 application/octet-stream

print "Please start snapchat on your device and go to the conversation of the message you wish to save/see. ~~DO NOT 'Tap to Load' yet~~"
print "Continue? (y/n)\n"
#Prompt y or n

#Get user's ip and use as variable for display here VVVVV
print "Route your device's traffic through a proxy (PC_IP:8080)..."
print "Please running 'mitmdump'..."

##########SUBPROCESS ADDED##################
#Hopefully, mitmdump is capturing flow
print "Capturing flows for 20 seconds"
print "Hit 'Tap to Load' on the desired snap"
#args=['q','-w','outfile']
#wish to see requests? exlude -q
proc = subprocess.Popen(['mitmdump','-q','-w','outfile'])#silent
#proc = subprocess.Popen(['mitmdump','-q','-w','outfile'])#verbose-ish
t = threading.Timer( 20.0, timeout, [proc] )
t.start()
t.join()
#############################################

###PARSE outfile###
#file io
#split on 


session=requests.Session()
### URLEncoded Form ###
#######################
print "\n~~~ URLEncoded Form data ~~~"
print "Snap post id:"
#check if 'r' in string (last char)
snapid = raw_input('')
#'id' is a reserved word -_-

print "\nReq_token:"
#check length?
req_token = raw_input('')

print "\nUnix timestamp:"
#Convert current time? - 
#eg. 1439057823280
timestamp = raw_input('')

print "\nYour username?"
username = raw_input('')

#print '\n'+str(prefilledURL)


#Header
print "\nPlease enter your Auth key:"
RAW_Auth_Token = raw_input('')
Auth_Token=str(str(RAW_Auth_Token).replace('\n','').replace(' ',''))

################NAME,##VALUE###########################
#Headers for POST request
headers = {
		'Host': 'feelinsonice-hrd.appspot.com',
	  	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
	 	'Connection': 'keep-alive',
	 	'Accept-Locale': 'en_US',
	 	'X-Snapchat-Client-Auth-Token': str(Auth_Token),
	  	'Proxy-Connection': 'keep-alive',
	  	'Accept': '*/*',
	  	'User-Agent': 'Snapchat/9.13.0.0 (iPhone6,1; iOS 8.1.2; gzip)',
	  	'Accept-Language': 'en;q=1',
	  	'Accept-Encoding': 'gzip'
	}
#'Content-Length', '138'


#Payload
data={'id': str(snapid),
	  'req_token': str(req_token),
	  'timestamp': str(timestamp),
	  'username': str(username)}

session.cookies.clear()
response=session.post(url,data=data,headers=headers)
#print response.text

snapPathFriendly=snapid.replace('/','_')

#Save picture to subdirectory instead of current folder with src
with open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg','wb') as f:
	f.write(response.content)
	f.close()

print "\nBlob-JPG saved to: "+os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg...\n'
img = Image.open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg')
img.show()
