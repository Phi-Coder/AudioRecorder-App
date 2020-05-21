import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from jnius import autoclass



# Initializing my my app
class AudioApp(App):
    def build(self):
        return AudioTool()

# My recorder class handles the audio recording process
class MyRecorder(self):

        #Recorder object to access android audio recorder    
        self.MediaRecorder = autoclass('android.media.MediaRecorder')
        self.AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        self.OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        self.AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

        # Record the Microphone with a 3GP recorder
        self.mRecorder = self.MediaRecorder()
        self.mRecorder.setAudioSource(self.AudioSource.MIC)
        self.mRecorder.setOutputFormat(self.OutputFormat.THREE_GPP)
        self.mRecorder.setOutputFile('/sdcard/MyAUDIO.3gp')
        self.mRecorder.setAudioEncoder(self.AudioEncoder.AMR_NB)
        self.mRecorder.prepare()

# audoo tool class which contains all the
class AudioTool(BoxLayout):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)

        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']  # quotes are not used
        self.switch = self.ids['duration_switch']
        self.user_input = self.ids['user_input']

        self.counter = ''  # don't know what is its function

    def enforce_numeric(self):
        if self.user_input.text.isdigit() == False:
            digit_list = [num for num in self.user_input.text if num.isdigit()]
            self.user_input.text = ''.join(digit_list)

    #Recording Function that calls the audio recorder
            
    def StartRecording(self,dt):
        self.r = MyRecorder() # create the recorder objects
        self.r.mRecorder.start() #start the recording by starting the 'mRecorder'

    
    # start recording clock button

    def StartRecording_clock(self):
        self.zero = 1  # resets the function if gets called more then once
        self.mins = 0  # reset the minutes on our timer
        self.duration = int(self.user_input.text)  # set the duration as user input

        Clock.schedule_interval(self.updateDisplay, 1)  # update after every sec
        Clock.schedule_once(self.StartRecording)
        self.start_button.disabled = True

        self.stop_button.disabled = False  # no info
        self.switch.disabled = True

    # stop recording clock button
    def StopRecording(self):

        Clock.unschedule(self.updateDisplay)
        Clock.unschedule(self.StartRecording)
        self.start_button.disabled = False
        self.switch.disabled = False

        self.display_label.text = 'Finished Recording'

    # Updating display at every new value

    def updateDisplay(self, dt):  # delta time(dt)

        # when switch is off ,simple recording
        if self.switch.active == False:
            if self.zero < 60 and len(str(self.zero)) == 1:
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.zero)
                self.zero += 1
            elif self.zero < 60 and len(str(self.zero)) == 2:
                self.display_label.text = '0' + str(self.mins) + ":" + str(self.zero)
                self.zero += 1
            elif self.zero == 60:
                self.mins += 1
                self.display_label.text = '0' + str(self.mins) + ':00'
                self.zero = 1


        # when switch is set on ,timer recording

        elif self.switch.active == True:
            if self.duration == 0:
                self.display_label.text = "Recording Finished!"
                self.StopRecording()

            elif self.duration > 0 and len(str(self.duration)) == 1:
                self.display_label.text = '00' + ':0' + str(self.duration)
                self.duration -= 1

            elif self.duration > 0 and self.duration < 60 and len(str(self.duration)) == 2:
                self.display_label.text = '00' + ':' + str(self.duration)
                self.duration -= 1

            elif self.duration >= 60 and len(str(self.duration % 60)) == 1:
                self.mins = int(self.duration / 60)
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.duration % 60)
                self.duration -= 1

            elif self.duration >= 60 and len(str(self.duration % 60)) == 2:
                self.mins = int(self.duration / 60)
                self.display_label.text = '0' + str(self.mins) + ':' + str(self.duration % 60)
                self.duration -= 1


# Running my app
if __name__ == '__main__':
    AudioApp().run()
