from pygame import *

class Message(object):

	def __init__(self, display):
		self.display = display
		self.background = image.load("assets/textBox.png").convert_alpha()
		self.font = font.Font("assets/fonts/Arcon.otf", 20)
		self.black = (0,0,0)

	def botMessage(self,text):
		self.display.blit(self.background, (0,360))

		self.display.blit(self.font.render(text, True, self.black), (250,390))
		print("Are you ready?")