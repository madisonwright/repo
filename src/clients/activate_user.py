#! /usr/bin/python3

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode


def main():
    # Check the CLI arguments
    if len(sys.argv)<4 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['mytext']  = sys.argv[2]
    args['pass'] = sys.argv[3]
    if sys.argv[4] == 'facofc':
        args['role'] = 'Facilities Officer'
    else:
        args['role'] = 'Logistics Officer'

    # Print a message to let the user know what is being tried
    print("Activating user: %s"%args['mytext'])

    # Setup the data to send
    data = urlencode(args)
    
    
    myroute = sys.argv[1] + 'activate_user' 
    req = Request(myroute,data.encode('ascii'),method='POST')


    #activate
    res = urlopen(req)

    result = res.read()
    if result == bytes('t','utf-8'):
        print("User successfully activated")
    elif result == bytes('p','utf-8'):
        print("Unable to create user; password too long")
    else:
        print("Unable to create user; username too long")

    
if __name__=='__main__':
    main()

