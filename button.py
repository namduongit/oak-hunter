import pygame

class Button():
	def __init__(self,x, y, image, image_hover, scale):
		self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
		self.image_hover = pygame.transform.scale(image_hover, (int(image.get_width() * scale), int(image.get_height() * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		surface.blit(self.image, (self.rect.x, self.rect.y))
		#get mouse position
		pos = pygame.mouse.get_pos()
		# Kiểm tra chuột có ấn hay di chuyển vào khu vực không để đổi hình ảnh
		if self.rect.collidepoint(pos):
			if self.image_hover:
						surface.blit(self.image_hover, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		return action


