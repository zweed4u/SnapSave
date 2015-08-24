#Flags for later
ua='nullDefault';
token='nullDefault';
uuid='nullDefault';
prefill='nullDefault';

#Throw in list/array to make check easier with an 'if any()'
items=[ua,token,uuid,prefill]

#Read file
with open('outfile', 'r') as inF:
    for index, line in enumerate(inF):
	#Hot word - Narrows our focus
        host = "/bq/blob"
	#Scary string manipulation - hopefully the format is the same for everyone
        if host in line:
		ua=line.split('User-Agent,')[1].split(':')[1].split(',]')[0];
		token="v3"+line.split('X-Snapchat-Client-Auth-Token,')[1].split(':v3')[1].split(',]')[0];
		uuid=line.split('X-Snapchat-UUID,')[1].split(':')[1].split(',]')[0];
		prefill='?'+'id='+line.split('content')[1].split(':id=')[1].split(',')[0];	

#Update list with possible changed vars
items=[ua,token,uuid,prefill]

#Check if any vars in list have default flag
if any(x in 'nullDefault' for x in items):
	print "Sorry, data not found\nAre you sure you loaded the snap?";
else:	
	print "\nUA: " + ua;
	print "\nAuth_token: "+token;
	print "\nUUID: "+uuid;
	print "\nPrefill query string: "+prefill;
	print "\n";
