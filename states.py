from transitions import Machine,State
import config
from DbHandler import get_states


class StateMachine():
	def __init__(self):
		pass

sm=StateMachine()
m=Machine(sm,config.states)




