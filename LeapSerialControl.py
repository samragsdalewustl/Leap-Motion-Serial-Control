import os, Leap, sys, thread, time, serial, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
	finger_names =['Thumb','Index','Middle','Ring','Pinky']
	bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
	state_names = ['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END'] 

	#global STATE_INVALID = -1
	#global STATE_START = 1
	#global STATE_UPDATE = 2
	#global STATE_END = 3

	SERIAL_PORT_NAME = "COM6" #Eventually switch this out for something dynamic
	VOLUME_CYCLE_AMOUNT = 10 #amount each finger cycle changes volume
	volume = 0 #always between 0 and 100
	lastVolume = 0; #Volume last sent to arduino
	VOLUME_DELTA = 2; #How often to send updates to the arduino
	SERIAL_SEND_TIMEOUT = .05 #Time between serial signals (excessive serial writes get DISCARDED)
	lastSerialTime = 0;



	def on_init(self, controller):
		print ("Initialized")
		#attempt arduino serial connection
		try:
			self.serialData = serial.Serial(self.SERIAL_PORT_NAME,9600)
			print "Arduino Connected"
		except:
			print "Arduino not connected on " + self.SERIAL_PORT_NAME
			sys.exit("ENDING: No Arduino = No execute-o")


	def on_connect(self, controller):
		print ("Motion sensor connected")

		#Enable all gestures, they may not all be used but there is no loss in a full enable
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

		#makes sure the program still gets leap motion frames while 
		#program runs in background. Ex: Computer using chrome
		controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

	def on_disconnect(self, controller):
		print ("Motion sensor disconnected")

	def on_exit(self, controller):
		print ("Exited")

	#every time there is a new frame of data this is called
	def on_frame(self,controller):
		frame = controller.frame()

		#go through each recognized gesture
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)

				#circle.state == 3 means the ircle has stopped, therefore, don't worry about action on that gesture
				if circle.state == gesture.STATE_STOP: 
					pass


				#if the circle has begun, set the swept angle to starting point (0)
				if circle.state == gesture.STATE_START:
					swept_angle = 0

				#if the state needs to be updated
				if circle.state == gesture.STATE_UPDATE:
					#retrieves the previous position of the circle gesture (frame(1))
					previous = CircleGesture(controller.frame(1).gesture(circle.id))
					#increases the swept angle
					#swept_angle = (circle.progress - previous.progress)*2*Leap.PI

					#if the gesture is clockwise volume should increase over the course of the gesture
					if circle.pointable.direction.angle_to(circle.normal) <=  Leap.PI/2:
						clockwiseness = "clockwise"
						#set the volume to either the increased volume or if it is too high, the max volume (99)
						self.volume = (min(self.volume+(circle.progress-previous.progress)*self.VOLUME_CYCLE_AMOUNT,99)); #volume increased: maximized at 100
					#if the gesture is counter-clockwise the volume should decrease over the course of the gesture
					else:
						clockwiseness = "counter-clockwise"
						#set the volume to either the decreased volume or if it is too low, the minimum volume (0)
						self.volume = (max(self.volume-(circle.progress-previous.progress)*self.VOLUME_CYCLE_AMOUNT,0));

				#print self.volume

				#If the volume change is greater than the serial send threshold (VOLUME_DELTA)
				#then send the data to the arduino
				if abs(self.volume-self.lastVolume) > self.VOLUME_DELTA or self.volume > 98 or self.volume < 1:
					print "Serialing" #for debug
					self.lastVolume = self.volume
					self.serialData.write('V'+chr(int(self.volume)))
					print 'V'+chr(int(self.volume)) #converts integer to a single ascii character and sends to arduino as string


			#Detect swipe gestures
			#Swiping right turns the lights on
			#Swiping left turns the lights off
			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)

				#for DEBUG
				#print "Swipe ID: " + str(swipe.id) + " State:" + str(self.state_names[swipe.state]) + " Position: " + str(swipe.position) + " Direction: " + str(swipe.direction) + " Speed(mm/s): " + str(swipe.speed)

				#consider doing below based on speed rather than distance delta
				if swipe.state == gesture.STATE_START: #swipe has started
					if abs(swipe.direction.x) > abs(swipe.direction.y):
						#if swipe is to the right
						if swipe.direction.x > .5 :
							#turn on lights
							#come up with new serial protocol MAYBE function
							self.sendSerial(str(1))

						#if swipe is to the left
						elif swipe.direction.x < -0.5:
							#turn off  lights
							self.sendSerial(str(0))
	
	#sends serial strings to arduino
	#will not send if called more often than SERIAL_SEND_TIMEOUT
	def sendSerial(self, msg):
		#confirms that enough time has elapsed to send more to serial
		if time.time() - self.lastSerialTime < self.SERIAL_SEND_TIMEOUT:
			return
		self.lastSerialTime = time.time()

		connected = True

		#if serial write fails, the connection needs to be closed and reestablished
		try:
			self.serialData.write(msg)
		except:
			connected = False

		if not connected:
			print("Reconnecting to arduino")

			self.serialData.close()
			self.serialData = serial.Serial(self.SERIAL_PORT_NAME, 9600)
			self.serialData.write(msg)

def main():
	#create listener and controller objects
	listener = LeapMotionListener()
	controller = Leap.Controller()
	controller.add_listener(listener)

	#kills program on cmd line return
	print ("Press enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		#remove listener
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()