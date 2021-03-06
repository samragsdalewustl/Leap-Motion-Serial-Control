import os, Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
	finger_anmes =['Thumb','Index','Middle','Ring','Pinky']
	bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
	state_names = ['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END']

	def on_init(self, controller):
		print ("Initialized")

	def on_connect(self, controller):
		print ("Motion sensor connected")

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print ("Motion sensor disconnected")

	def on_exit(self, controller):
		print ("Exited")

	def on_frame(self,controller):
		frame = controller.frame()

		"""print ("Frame ID: " + str(frame.id)\
			+ "Time stamp: " + str(frame.timestamp)\
			+ " # hands: " + str(len(frame.hands))\
			+ " # fingers: " + str(len(frame.fingers))\
			+ " # tools: " + str(len(frame.tools))\
			+ " # gestures: " + str(len(frame.gestures()))); """

		for hand in frame.hands

def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()

	controller.add_listener(listener)

	print ("Press enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()