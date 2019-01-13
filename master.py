#! /usr/bin/python3.5
import os
import sys
import time


WORK_DIR = '/home/pi/ras_1901/'

#sys.path.append(WORK_DIR)
#sys.path.append(WORK_DIR+'lib/')

# Hardware Components imports
from lib import Display, CardReader, PasBuz, Button

# Software Tasks imports
from lib import Clocking, Odooxlm, ShowRFID, Menu

# I/O PINS DEFINITION on the RPi Zero W
# Using the BOARD numbering system, which uses the pin numbers on the
# P1 Header of the RPi board.
#
# Advantage: the hardware will always work, regardless of the
# board revision of the RPi: no need to rewire or change the code.

PinSignalBuzzer = 13  # Buzzer
PinPowerBuzzer  = 12

PinSignalDown   = 31  # DOWN button
PinPowerDown    = 35

PinSignalOK     = 29  # OK button signal
PinPowerOK      = 35


# Creating Instances for the HARDWARE COMPONENTS

Buz      = PasBuz.PasBuz( PinSignalBuzzer, PinPowerBuzzer )

Disp     = Display.Display()
               # the Display Type - for example: OLED SH1106
               # is defined in the Class

Reader   = CardReader.CardReader()

B_Down   = Button.Button( PinSignalDown, PinPowerDown )

B_OK     = Button.Button( PinSignalOK, PinPowerOK )

# Creating Instances for the SOFTWARE TASKS


Odoo     = Odooxlm.Odooxlm( WORK_DIR )
               # communicate to Odoo via xlm
               #
               # data.json lives in WORK_DIR : the parameters
               # to communicate with odoo are stored there

Clock    = Clocking.Clocking( Disp, Reader, Odoo, Buz )
               # Main Functions of the Terminal:
               # Show Time and do the clockings (check in/out)
               #
               # There are two modes of operation possible and switchable
               # through an instance flag: synchronous mode (standard)
               # and asynchronous mode.

ShowRFID = ShowRFID.ShowRFID( Disp, Reader, Odoo, Buz )
               # Display the RFID code (in HEX) of the swiped card

Menu     = Menu.Menu( Clock , ShowRFID )
               # This Menu is shown when the Terminal (RAS)
               # is switched On or when the Admin Card is swiped.
               # It allows to switch between the different
               # Functions/Tasks available

#            MAIN LOOP            #
#     RFID Attendance Terminal    #

# The Main Loop only ends when the option to reboot is chosen.
#
# In all the Tasks, when the Admin Card is swiped,
# the program returns to this Loop,
# where a new Task can be selected using the OK and Down Buttons.

Disp.testing()

"""
while not ( Menu.reboot == True ):
                          # The Main Loop only ends
                          # when the option
                          # to reboot is chosen.

   Disp.show_message( Menu.action[Menu.option] )
               # The Task that can be selected when
               # pressing the OK Button is shown on the Display

   if B_OK.pressed:       # When the Button OK is pressed

       Buz.Play('OK')     # Acoustic Feedback
                          # that the OK Button was pressed

       # WE WANT TO BE SURE ###############################
       Disp.show_message('sure?')

       B_OK.pressed     = False # avoid false positives
       B_Down.pressed   = False

       while not ( B_OK.pressed or B_Down.pressed): # wait for an answer
           B_Down.scanning() # If no Button was Pressed continue scanning
           B_OK.scanning()   # if the Buttons are pressed

       if B_OK.pressed:    # the OK Button was pressed for
                           # a second time

           Buz.Play('OK')

           B_Down.poweroff() # Swith Buttons Power off
           B_OK.poweroff()   # to keep the electronics cool

           Menu.selected() # The selected Task is run.
                           # When the Admin Card is swiped
                           # the Program returns here again.

           Buz.Play('OK')  # Acoustic Feedback to mark the end of the Task
                           # and the coming back to the menu
           B_Down.poweron()   # switch the Buttons back on
           B_OK.poweron()     # to detect what the user wants

       else:

           Buz.Play('down')

       B_OK.pressed     = False # avoid false positives
       B_Down.pressed   = False

   elif B_Down.pressed:   # When the Button Down is pressed

       Buz.Play('down')   # Acoustic Feedback
                          # that the Down Button was pressed

       Menu.down()

   B_Down.scanning()      # If no Button was Pressed continue scanning
   B_OK.scanning()        # if the Buttons are pressed

#---------------------------------#
#                                 #
#            REBOOTING            #
#                                 #
#---------------------------------#

# Disp.show_message('shut_down')
# time.sleep(3)

# print('reboot')

"""