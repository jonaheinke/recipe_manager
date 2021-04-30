import os

def resetcwd():
	os.chdir(os.path.dirname(os.path.realpath(__file__))) #TODO: This should sadly set the cwd to the location of util.py and not of the executing program.

class LocalPath:
	def __init__(self, path = None):
		self.target = path
	
	def __enter__(self):
		self.origin = os.getcwd()
		if self.target is not None:
			os.chdir(self.target)
		return self
	
	def cd(self, path):
		os.chdir(path)

	def __exit__(self, *_): #type, value, traceback
		os.chdir(self.origin)
	
	#Potentially useful operations

	def __repr__(self):
		return os.getcwd()