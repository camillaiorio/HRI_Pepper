#http://doc.aldebaran.com/2-5/naoqi/motion/control-walk-api.html

import qi
import argparse
import sys
import time
import math
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1',
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    print "Connecting to tcp://" + pip + ":" + str(pport)

	#Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Move", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session



    #Starting services
    motion_service = session.service("ALMotion")

    print 'Stop'

    motion_service.stopMove() 
    


if __name__ == "__main__":
    main()

