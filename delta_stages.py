# Two stage example Virtual Machine file
# moves get set in Main
# usb port needs to be set in initInterfaces
# Nadya Peek Dec 2014

# modified for three stages a,b,c since we seem to a delta printer
# ys

#------IMPORTS-------
from pygestalt import nodes
from pygestalt import interfaces
from pygestalt import machines
from pygestalt import functions
from pygestalt.machines import elements
from pygestalt.machines import kinematics
from pygestalt.machines import state
from pygestalt.utilities import notice
from pygestalt.publish import rpc	#remote procedure call dispatcher
import time
import io


#------VIRTUAL MACHINE------
class virtualMachine(machines.virtualMachine):

	#############
	# NEED to change usb port
	#############
	def initInterfaces(self):
		if self.providedInterface: self.fabnet = self.providedInterface		#providedInterface is defined in the virtualMachine class.
	else: self.fabnet = interfaces.gestaltInterface('FABNET', interfaces.serialInterface(baudRate = 115200, interfaceType = 'ftdi', portName = '/dev/ttyUSB0'))

	def initControllers(self):
		# should we call it xyz for delta? alpha beta gamma?

		self.alphaNode = nodes.networkedGestaltNode('node  alpha',self.fabnet,filename='086-005a.py',persistance=self.persistance)
		self.alphaNode = nodes.networkedGestaltNode('node  beta',self.fabnet,filename='086-005a.py',persistance=self.persistance)
		self.alphaNode = nodes.networkedGestaltNode('node  gamma',self.fabnet,filename='086-005a.py',persistance=self.persistance)

		self.abgNode = nodes.compoundNode(self.alphaNode, self.betaNode, self.gammaNode)

	def initCoordinates(self):
		self.position = state.coordinate(['mm', 'mm', 'mm'])

	def initKinematics(self):
		self.aAxis = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(8), elements.invert.forward(True)])
		self.bAxis = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(8), elements.invert.forward(False)])
		self.gAxis = elements.elementChain.forward([elements.microstep.forward(4), elements.stepper.forward(1.8), elements.leadscrew.forward(8), elements.invert.forward(False)])

		#creates a identity matrix with the order of three
		self.stageKinematics = kinematics.direct(3)	#direct drive on all axes

	def initFunctions(self):
		self.move = functions.move(virtualMachine = self, virtualNode = self.xyNode, axes = [self.xAxis, self.yAxis], kinematics = self.stageKinematics, machinePosition = self.position,planner = 'null')
		self.jog = functions.jog(self.move)	#an incremental wrapper for the move function
		pass

	def initLast(self):
		#self.machineControl.setMotorCurrents(aCurrent = 0.8, bCurrent = 0.8, cCurrent = 0.8)
		#self.xNode.setVelocityRequest(0)	#clear velocity on nodes. Eventually this will be put in the motion planner on initialization to match state.
		pass

	def publish(self):
		#self.publisher.addNodes(self.machineControl)
		pass

	def getPosition(self):
		return {'position':self.position.future()}

	def setPosition(self, position  = [None]):
		self.position.future.set(position)

	def setSpindleSpeed(self, speedFraction):
		#self.machineControl.pwmRequest(speedFraction)
		pass

#------IF RUN DIRECTLY FROM TERMINAL------
if __name__ == '__main__':
	# The persistence file remembers the node you set. It'll generate the first time you run the
	# file. If you are hooking up a new node, delete the previous persistence file.
	stages = virtualMachine(persistenceFile = "test.vmp")

	# You can load a new program onto the nodes if you are so inclined. This is currently set to
	# the path to the 086-005 repository on Nadya's machine.
	#stages.xyNode.loadProgram('../../../086-005/086-005a.hex')

	# This is a widget for setting the potentiometer to set the motor current limit on the nodes.
	# The A4982 has max 2A of current, running the widget will interactively help you set.
	#stages.xyNode.setMotorCurrent(0.7)

	# This is for how fast the
	stages.xyNode.setVelocityRequest(8)

	# Some random moves to test with
	moves = [[10,10],[20,20],[10,10],[0,0]]

	# Move!
	for move in moves:
		stages.move(move, 0)
		status = stages.xAxisNode.spinStatusRequest()
		# This checks to see if the move is done.
		while status['stepsRemaining'] > 0:
			time.sleep(0.001)
			status = stages.xAxisNode.spinStatusRequest()
