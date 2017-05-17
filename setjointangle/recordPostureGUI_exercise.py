#MODULES USED IN THIS PROGRAM
#http://doc.aldebaran.com/2-5/naoqi/motion/alrobotposture-api.html
#http://doc.aldebaran.com/2-5/naoqi/motion/control-joint-api.html

from Tkinter import *
import qi
import argparse
import sys
import time

jointsNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

#joint limits for Pepper, taken from http://doc.aldebaran.com/2-5/family/pepper_technical/joints_pep.html
jointLimits ={'HeadYaw': (-2.0857, 2.0857),
              'HeadPitch': (-0.7068, 0.6371),
              'LShoulderPitch': (-2.0857, 2.0857),
              'LShoulderRoll': (0.0087, 1.5620),
              'LElbowYaw': (-2.0857, 2.0857),
              'LElbowRoll': (-1.5620, -0.0087),
              'LWristYaw': (-1.8239, 1.8239),
              'RShoulderPitch': (-2.0857, 2.0857),
              'RShoulderRoll': (-1.5620, -0.0087),
              'RElbowYaw': (-2.0857, 2.0857),
              'RElbowRoll': (0.0087,1.5620),
              'RWristYaw': (-1.8239, 1.8239)}

#Variable to store the saved postures
postures = {}
class JointAnglesGUI:

    def __init__(self, master, motion_service, posture_service):
        self.master = master
        master.title("Joint Angles GUI")
        self.motion_service = motion_service
        self.posture_service = posture_service

        self.labels = []
        self.scalewidgets = []

        #TODO: Read initial angle values 
        # initSensorAngles = ....
        initSensorAngles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #
        print "Joints sensors readings:"
        for j, jointname in enumerate(jointsNames):
            print (jointname, str(initSensorAngles[j]))

            self.labels.append(Label(text=jointname))
            self.labels[j].grid(row=j, column=1)
            self.scalewidgets.append(Scale(master, from_=jointLimits[jointname][0], to=jointLimits[jointname][1], resolution=0.1, orient="horizontal", length=200))
            self.scalewidgets[j].set(float(initSensorAngles[j]))
            self.scalewidgets[j].bind("<ButtonRelease-1>", lambda event, widget = self.scalewidgets[j], jointname = jointsNames[j]: self.applyAngle(event, widget, jointname))
            self.scalewidgets[j].grid(row=j, column=2)

        #Storing the initial position
        namePosture = 'Init'
        postures[namePosture]=initSensorAngles
            
        self.buttonreset = Button(self.master, text="Reset", command=self.callbackReset)
        self.buttonreset.grid(row=len(jointsNames)+1, column=1)
        self.buttonsave = Button(self.master, text="Save", command=self.callbackSave)
        self.buttonsave.grid(row=len(jointsNames)+1, column=2)

        self.labelposture = Label(text="Select Posture")
        self.labelposture.grid(row=len(jointsNames)+2,column=1)
        self.posturesmenu_var = StringVar(self.master)
        self.posturesmenu_var.set(postures.keys()[0])
        self.posturesmenu = OptionMenu(self.master, self.posturesmenu_var, postures.keys()[0], command = self.gotoPostureSelected)
        self.posturesmenu.configure(width=20)
        self.posturesmenu.grid(row=len(jointsNames)+2,column=2)
            
    def applyAngle(self, event, widget, jointname):
        print "setting", jointname, "to: ", widget.get()
        angle = widget.get()
        # TODO: complete by applying the selected angle to the robot
        # ....
        #
        
    def callbackReset(self):
        print "click!"
        # TODO: Use a ALRobotPosture to go to posture "Stand"
        # ....
        #

        # TODO: update value of the scalewidgets by reading the sensors
        # ....
        
    def callbackSave(self):
        print "click!"
        # TODO: Read angles of all joints
        # savedPosture = ....
        savedPosture = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #
        print savedPosture
        #Storing posture
        namePosture = 'Posture'+str(len(postures))
        postures[namePosture]=savedPosture
        print postures.keys()
        self.updatePosturesMenu(namePosture)

    def updatePosturesMenu(self, posture):
        menu=self.posturesmenu['menu']
        menu.add_command(label=posture, command=lambda v=posture: self.gotoPostureSelected(v))
        
    def gotoPostureSelected(self, posture):
        self.posturesmenu_var.set(posture)
        print self.posturesmenu_var.get()
        print "doing something"

        #TODO: Apply selected posture
        # ....
        #


class AngleController:
    def __init__(self,master):
        self.master = master
        parser = argparse.ArgumentParser()
        parser.add_argument("--pip", type=str, default="127.0.0.1",
                            help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
        parser.add_argument("--pport", type=int, default=9559,
                            help="Naoqi port number")
        args = parser.parse_args()
        pip = args.pip
        pport = args.pport

        #Starting session
        session = qi.Session()
        try:
            session.connect("tcp://" + pip + ":" + str(pport))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        #Starting services
        self.motion_service  = session.service("ALMotion")
        self.posture_service = session.service("ALRobotPosture")
        
        gui = JointAnglesGUI(self.master, self.motion_service, self.posture_service)
        master.mainloop()
       
    
if __name__ == "__main__":
    master = Tk()
    ac = AngleController(master)
