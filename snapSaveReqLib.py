import os, requests, time, errno, subprocess, threading, socket, paramiko, sys
from PIL import Image
from scp import SCPClient

#SSHv2 in Python
debInstall=raw_input("Do you need to install SSL KillSwitch? (y/n) ")
if debInstall=='y' or debInstall=='Y':
	relPath=os.getcwd()
	iphone_ip=raw_input("What is your iphone's ip? (Settings>Wi-Fi>i>IP Address) ")
	iphone_pw=raw_input("What is your iphone's root password? ('alpine' by default) ")

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(str(iphone_ip), username='root', password=str(iphone_pw))

	scp = SCPClient(ssh.get_transport())

	scp.put(relPath+'/com.nablac0d3.SSLKillSwitch2_0.10.deb','com.nablac0d3.SSLKillSwitch2_0.10.deb.deb')
	stdin, stdout, stderr = ssh.exec_command('dpkg -i com.nablac0d3.SSLKillSwitch2_0.10.deb.deb')
	print '\n'
	for i in stdout.readlines():
		print i
	print '\n'
elif debInstall=='n' or debInstall=='N':
	pass
else:
	print "\nPlease rerun and enter 'y' or 'n' when prompted.\n"
	sys.exit()


myLocalIP=([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

#Flags for parse
ua='nullDefault';token='nullDefault';uuid='nullDefault';prefill='nullDefault';funcFlag='0';

#Throw in list/array to make check easier with an 'if any()'
items=[ua,token,uuid,prefill]

def timeout( p ):
	if p.poll() is None:
        	try:
        		p.kill()
        	        print '10 seconds are up! --terminating'
       		except OSError as e: #race condition
                	if e.errno != errno.ESRCH:
                		raise

def outfileParse(items,ua,token,uuid,prefill,funcFlag):
	#Read file
	with open('outfile', 'r') as inF:
	    for index, line in enumerate(inF):
		#Hot word - Narrows our focus
		host = "/bq/blob"
		#Scary string manipulation - hopefully the format is the same for everyone
		if host in line:
			ua=line.split('User-Agent,')[1].split(':')[1].split(',]')[0];
			token="v5"+line.split('X-Snapchat-Client-Auth-Token,')[1].split(':v5')[1].split(',]')[0];
			uuid=line.split('X-Snapchat-UUID,')[1].split(':')[1].split(',]')[0];
			prefill='?'+'id='+line.split('content')[1].split(':id=')[1].split(',')[0];	

	#Update list with possible changed vars
	items=[ua,token,uuid,prefill]
	#Check if any vars in list have default flag
	if any(x in 'nullDefault' for x in items):
		print "Sorry, data not found\nAre you sure you loaded the snap?";
		return funcFlag;
	else:	
		#print "Values should have changed. =)"
		funcFlag='1';
		return items;

url='https://feelinsonice-hrd.appspot.com/bq/blob'
# 200 application/octet-stream

#Get user's ip and use as variable for display here VVVVV
print "Please visit 'http://www.mitm.it' on your device and install the mitmproxy certificate.\n"
print "Route your device's traffic through an http proxy ("+str(myLocalIP)+":8080)... Make sure it's on the same wireless network as this PC\n"
print "On iPhone:\nSettings>SSL Kill Switch 2>Enable 'Disable Certificate Validation'\n\nSettings> Wi-Fi> [your network]> HTTP PROXY> Manual"
print "Server: " +str(myLocalIP)+'\nPort: 8080\nAuthentication: OFF\n'
print "Please start snapchat on your device and go to the conversation of the message you wish to save/see. ~~DO NOT 'Tap to Load' yet~~"
raw_input("Please press Enter when you're in the correct thread/conversation of the desired snap\n")
raw_input("Please press Enter to begin capture of flows.\nYou'll have 10 seconds.\nDuring this time you just need to 'Tap to Load' the snap you wish to see/save.\n")

##########SUBPROCESS ADDED##################
#Hopefully, mitmdump is capturing flow
print "Capturing flows for 10 seconds"
print "Hit 'Tap to Load' on the desired snap"
#args=['q','-w','outfile']
#wish to see requests? exlude -q
proc = subprocess.Popen(['mitmdump','-q','-w','outfile'])#silent
#proc = subprocess.Popen(['mitmdump','-w','outfile'])#verbose-ish
t = threading.Timer( 10.0, timeout, [proc] )
t.start()
t.join()
#############################################

###PARSE outfile###
items=outfileParse(items,ua,token,uuid,prefill,funcFlag);

##Check if null defual in any index -- if so terminate.
ua=items[0];
token=items[1];
uuid=items[2];
prefill=items[3];
#if funcFlag='0' ~~~ redo term program -- else continue parse

session=requests.Session()

### URLEncoded Form ###
#######################
snapid = prefill.split('=')[1].split('&')[0];
req_token = prefill.split('=')[2].split('&')[0];
timestamp = prefill.split('=')[3].split('&')[0];
username =  prefill.split('=')[4].split('&')[0];

################NAME,##VALUE###########################
#Headers for POST request
headers = {
		'Host': 'feelinsonice-hrd.appspot.com',
	  	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
	 	'Connection': 'keep-alive',
	 	'Accept-Locale': 'en_US',
	 	'X-Snapchat-Client-Auth-Token':token,
	  	'Proxy-Connection': 'keep-alive',
	  	'Accept': '*/*',
	  	'User-Agent': ua,
	  	'Accept-Language': 'en;q=1',
	  	'Accept-Encoding': 'gzip'
	}
#'Content-Length', '138'
#'X-Snapchat-UUID', uuid

#Payload
data={'id': snapid,
	  'req_token': req_token,
	  'timestamp': timestamp,
	  'username': username}

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
