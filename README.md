# SnapSave  
<p align="center">
  <img src="https://github.com/zweed4u/SnapSave/blob/master/snap.png?raw=true" alt="Snap me! @ZWeed4U"/>
</p>

"They’ll view it, laugh, and then the Snap disappears from the screen – unless they take a screenshot!"...or do 'they'? 

SnapSave allows *somewhat* savvy users to replicate a request when loading a snap.  
All you need is mitmproxy!  
Route traffic from your device through a proxy, open snapchat, 'tap to load' the snap of interest and ~~seek how to replicate.~~ let snapSave do the rest.  
* Two Scripts, Two Libraries! (sorta)
 * Pick your poison with either the urllib module or the request library  
* Requires network sniffing to obtain necessary values of fields in the POST form used in viewing a snap  
* Adds required headers to return the snap binary blob in jpg form  

Tested on v9.14.2.0 via iOS 8.1.2  
9.20.X supports ca pinning which kills traffic sniffing. Downgrade to an earlier ipa.  
However, a ping request is observable and returns. See png  
Future updates will allow more flexiblity in locale as well as allow for story downloads amongst other things.  

Contact/Follow: [@ZWeed4U](http://www.twitter.com/zweed4u)

