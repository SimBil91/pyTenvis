import urllib2

class TenvisInput():
    
    def __init__(self, domain, uri_format, user, pwd):
        """ domain:   Camera IP address or web domain 
                      (e.g. 385345.kaicong.info)
        """
        self.running = False
        self.uri = uri_format.format(user, pwd, domain)
        print(self.uri)
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        passman.add_password(None, self.uri, user, pwd)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # create the AuthHandler
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        
        
