#! /usr/bin/python3

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode


def main():
    # Check the CLI arguments
    if len(sys.argv)<2 :
        print("Usage: python3 %s <url> <username>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['mytext']  = sys.argv[2]

    # Print a message to let the user know what is being tried
    print("Revoking user: %s"%args['mytext'])

    # Setup the data to send
    data = urlencode(args)
    
    
    myroute = sys.argv[1] + 'revoke_user' 
    req = Request(myroute,data.encode('ascii'),method='POST')


    #activate
    res = urlopen(req)
    
    result = res.read()
    if result == bytes('t','utf-8'):
        print("User successfully revoked")
    else:
        print("Unable to revoke user; user does not exist")
    
if __name__=='__main__':
    main()

