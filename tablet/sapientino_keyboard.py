#http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

import qi
import argparse
import sys
import os
import math

commands = [ ['F', 620, 130], ['B', 620, 500], ['L', 480, 310], ['R', 820, 310],
['OK', 620, 310], ['X', 480, 500], ['A', 820, 500] ]

tts_service = None
motion_service = None

plan = []
flag_run = False

def reset():
    global plan, flag_run
    plan = []
    flag_run = False


def forward(r=1):
    print 'forward',r
    #Move in its X direction
    x = r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def backward(r=1):
    print 'backward',r
    x = -r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def left(r=1):
    print 'left',r
    #Turn 90deg to the left
    x = 0.0
    y = 0.0
    theta = math.pi/2
    motion_service.moveTo(x, y, theta) #blocking function

def right(r=1):
    print 'right',r
    #Turn 90deg to the right
    x = 0.0
    y = 0.0
    theta = -math.pi/2
    motion_service.moveTo(x, y, theta) #blocking function


def say_command(cmd):
    global tts_service
    if (cmd=='F'):
        tts_service.say("Avanti")
    if (cmd=='B'):
        tts_service.say("Indietro")
    if (cmd=='L'):
        tts_service.say("Sinistra")
    if (cmd=='R'):
        tts_service.say("Destra")
    if (cmd=='OK'):
        tts_service.say("OK.")
    if (cmd=='X'):
        tts_service.say("Missione cancellata. Riprova.")
    if (cmd=='A'):
        tts_service.say("Azione")

def say_plan(plan):
    global tts_service
    tts_service.say("Hai programmato la missione: ")
    for p in plan:
        say_command(p)
    tts_service.say("premi di nuovo il tasto OK per partire")


def exec_command(cmd):
    global tts_service
    if (cmd=='F'):
        forward()
    if (cmd=='B'):
        backward()
    if (cmd=='L'):
        left()
    if (cmd=='R'):
        right()
    if (cmd=='A'):
        tts_service.say("Azione")


def exec_plan(plan):
    global tts_service
    print "Execution ",plan
    tts_service.say("Missione avviata!!!")
    for p in plan:
        exec_command(p)
    tts_service.say("Missione compiuta. Pronto per una nuova missione.")
    reset()

# function called when the signal onTouchDown is triggered
def onTouched(x, y):
    global tts_service
    global plan, flag_run

    print "coordinates are x: ", x, " y: ", y
    mind=200
    cmd = ''
    for a in commands:
        d = abs(x - a[1]) + abs(y - a[2])
        if (d < mind):
            mind = d
            cmd = a[0]
    print 'Sapientino key: ',cmd
    say_command(cmd)
    if (cmd=='X'):
        reset()
    elif (cmd=='OK'):
        if (flag_run):
            exec_plan(plan)
        else:
            say_plan(plan)
            flag_run = True
    else:
	plan.append(cmd)
	print plan

    
def main():
    global tts_service, motion_service

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["TabletModule", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    motion_service = session.service("ALMotion")
    tablet_service = session.service("ALTabletService")

    tablet_service.showImage("http://198.18.0.1/apps/spqrel/img/sapdoc-buttons.jpg")

    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage("Italian")
    tts_service.say("ciao, sono il tuo amico Peppino.")
    tts_service.say("pronto per la programmazione.")

    idTTouch = tablet_service.onTouchDown.connect(onTouched)
    app.run()    



if __name__ == "__main__":
    main()
