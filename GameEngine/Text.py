# Hide pygame message
import sys, os

with open(os.devnull, 'w') as f:
	old_stdout = sys.stdout
	sys.stdout = f
	
	import pygame

	sys.stdout = old_stdout

class Text:
	@staticmethod
	def text(text, font, size, color=(255, 255, 255), owidth=None, ocolor=(0, 0, 0), antialias=False, bold=False, italic=False, background=False):
		'''
			Types: string, string, (number, number, number) -> pygame.Surface
		'''

		font = pygame.font.SysFont(font, size, bold=bold, italic=italic)

		if owidth != None and background:
			background = False
			outlineBackground = True

		text = font.render(text, antialias, color, background)

		if owidth != None:
			outline = Text.text(text, font, size + owidth, color=ocolor, antialias=antialias, bold=bold, italic=italic, background=outlineBackground)
			outline.blit(text)

			text = outline

		return text