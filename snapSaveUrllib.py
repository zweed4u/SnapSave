import os
import urllib
import urllib2
from PIL import Image

baseURL='https://feelinsonice-hrd.appspot.com/bq/blob'
# 200 application/octet-stream


print "Please start snapchat on your device and go to the conversation of the message you wish to save/see. ~~DO NOT 'Tap to Load' yet~~"
print "Continue? (y/n)"
#Prompt y or n

#Get user's ip and use as variable for display here VVVVV
print "Route your device's traffic through a proxy (PC_IP:8080)..."
print "Please run 'mitmdump -w outfile' we're going to grab necessary values for your headers and payload."
print "Continue? (y/n)"
#Prompt y or n

print "Hit 'Tap to Load' on the desired snap"
#Hopefully, mitmdump is capturing this flow
print "Has it finished loading? (Now reads 'Tap to View')"
#Prompt y or n - wait if n


###PARSE outfile###
#file io
#split on 




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

prefilledURL=str(baseURL)+'?id='+str(snapid)+'&req_token='+str(req_token)+'&timestamp='+str(timestamp)+'&username='+str(username)

#print '\n'+str(prefilledURL)

#Migrated to urllib2 for header capability
req = urllib2.Request(prefilledURL)

#Header
print "\nPlease enter your Auth key:"
RAW_Auth_Token = raw_input('')
Auth_Token=str(str(RAW_Auth_Token).replace('\n','').replace(' ',''))

################NAME,##VALUE###########################
req.add_header('Host', 'feelinsonice-hrd.appspot.com')
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
req.add_header('Connection', 'keep-alive')

#Prompt for language-Don't assume english
req.add_header('Accept-Locale', 'en_US')
req.add_header('X-Snapchat-Client-Auth-Token', str(Auth_Token))
req.add_header('Proxy-Connection', 'keep-alive')
req.add_header('Accept', '*/*')

#Prompt for version - phone - ios
req.add_header('User-Agent', 'Snapchat/9.13.0.0 (iPhone6,1; iOS 8.1.2; gzip)')

#Prompt for language-Don't assume english
req.add_header('Accept-Language', 'en;q=1')
req.add_header('Accept-Encoding', 'gzip')
#req.add_header('Content-Length', '138')

resp = urllib2.urlopen(req).read()
#print resp

snapPathFriendly=snapid.replace('/','_')

#Save picture to subdirectory instead of current folder with src
f=open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg','wb')
f.write(resp)
f.close()

print "\nBlob-JPG saved to: "+os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg\nOpening...\n'
img = Image.open(os.getcwd()+'/Blobs/'+str(snapPathFriendly)+'.jpg')
img.show()



