import sys 
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from time import sleep
import pygame.font





#fff Settings
class Settings():
	"""CLass store all settings"""

	def __init__(self):
		"""initilize the game settings"""
		#screen settings
		self.screen_Width = 1000
		self.screen_Height = 700
		self.bg_color = (230, 230, 230)


		#ship settings
		self.ship_speed_factor = 1
		self.ship_limit = 1

		#shooting bullets
		self.bullet_spreed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60,60,60
		self.bullets_allowed = 1

		# Alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# How quickly the game speeds up
		self.speedup_scale = 1.1
		self.initialize_dynamic_settings()

		# How quickly the alien point values increase
		self.score_scale = 1.5


	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
			
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1
		 
		# Scoring
		self.alien_points = 50


	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale	

		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)

#fae Game_stats
class GameStats():
	"""Track statistics for Alien Invasion."""
	def __init__(self, ai_settings):
		"""Initialize statistics."""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# # Start Alien Invasion in an active state.
		# self.game_active = True
		# Start game in an inactive state.
		self.game_active = False

		# High score should never be reset.
		self.high_score = 0
		
	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1


#fae Scoreboard
class Scoreboard():
	"""A class to report scoring information."""
	def __init__(self, ai_settings, screen, stats):
		"""Initialize scorekeeping attributes."""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		# Font settings for scoring information.
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		# Prepare the initial score images.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()


	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "high score: {:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.ai_settings.bg_color)
		
		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top


	def prep_score(self):
		"""Turn the score into a rendered image."""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "score: {:,}".format(rounded_score)
		# score_str = str(self.stats.score)
		

		self.score_image = self.font.render(score_str, True, self.text_color,self.ai_settings.bg_color)
		
		# Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_level(self):
		"""Turn the level into a rendered image."""
		level = int(round(self.stats.level))
		level = "level: {:,}".format(level)


		self.level_image = self.font.render(level,True,self.text_color, self.ai_settings.bg_color)
		# Position the level below the score.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10	

		
	def show_score(self):
		"""Draw score to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)	



#fae Button
class Button():
	def __init__(self, ai_settings, screen, msg):
		"""Initialize button attributes."""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		# Set the dimensions and properties of the button.
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)
		
		# Build the button's rect object and center it.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
		
		# The button message needs to be prepped only once.
		self.prep_msg(msg)


	def prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render(msg, True, self.text_color,
		self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)		


#ff0 Ship

class Ship():
	
	def __init__(self,screen,ai_settings):
		
		#Settings
		self.ai_settings = ai_settings
		

		"""initilize ship in start position"""
		self.screen = screen
		#load the ship image
		self.image = pygame.image.load("image/main_bird/bird.bmp")
		self.image = pygame.transform.scale(self.image,(200,100))	
		#get rect from size screen and image
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()


		#start ship bottom on the center screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom


		#store Decimal value ship center
		self.center = float(self.rect.centerx)
		#move flag
		self.moving_right = False
		self.moving_left = False

	
	def center_ship(self):
		"""Center the ship on the screen."""
		self.center = self.screen_rect.centerx	


	def update(self):
		"""update the ship position based on the movement flag"""
		if self.moving_right and self.rect.right < self.screen_rect.right+100:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > -100:
			self.center -= self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center	

	def blitme(self):
		"""draw ship current location"""	
		self.screen.blit(self.image, self.rect)


#ff0 Alien

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	def __init__(self, ai_settings, screen):
		"""Initialize the alien and set its starting position."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Load the alien image and set its rect attribute.
		self.image = pygame.image.load("image/enemy_bird/alien.bmp")
		self.image = pygame.transform.scale(self.image,(80,80))


		self.rect = self.image.get_rect()
		
		# Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# Store the alien's exact position.
		self.x = float(self.rect.x)
		
	
	def check_edges(self):
		"""Return True if alien is at edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True		

	def update(self):
		"""Move the alien right."""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x	

	def blitme(self):
		"""Draw the alien at its current location."""
		self.screen.blit(self.image, self.rect)






#ae3 Bullets

class Bullets(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self,ai_settings,screen,ship):
		
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = screen

		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,ai_settings.bullet_height)

		
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_spreed_factor


	def update(self):	
		"""move bullet on the screen"""
		#update decimal position
		self.y -= self.speed_factor
		#update the rect position
		self.rect.y = self.y


	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)











#f00 Functions
class functions():	

	#fff fun_Keys 
	def keydown_events(self,event, ai_settings, screen, ship, bullets):
		"""Respond to keypresses."""
		if event.key == pygame.K_RIGHT:
			ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self.fire_bullet(ai_settings, screen, ship, bullets)
		elif event.key == pygame.K_q:
			sys.exit()	

			

	def keyup_events(self,event,ship):
		"""Respond to key releases."""
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				ship.moving_right = False
			elif event.key == pygame.K_LEFT:
				ship.moving_left = False
	

	def check_events(self,ai_settings, screen, stats, sb, play_button, ship, aliens,bullets):
		#watch keyboard events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				#KEY DOWN
				self.keydown_events(event, ai_settings, screen, ship, bullets)
			elif event.type == pygame.KEYUP:
				#KEY UP
				self.keyup_events(event, ship)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				self.check_play_button(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets, mouse_x, mouse_y)

	
	def check_play_button(self,ai_settings, screen, stats, sb, play_button, ship,aliens, bullets, mouse_x, mouse_y):
		"""Start a new game when the player clicks Play."""

		button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
		if button_clicked and not stats.game_active:

			# Reset the game settings.
			ai_settings.initialize_dynamic_settings()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

			# Reset the game statistics.
			stats.reset_stats()
			stats.game_active = True

			# Reset the scoreboard images.
			sb.prep_score()
			sb.prep_high_score()
			sb.prep_level()


			# Empty the list of aliens and bullets.
			aliens.empty()
			bullets.empty()
			
			# Create a new fleet and center the ship.
			self.create_fleet(ai_settings, screen, ship, aliens)
			ship.center_ship()


	#fff fun_screen
	def update_screen(self,ai_settings, screen, stats, sb, ship, aliens, bullets,play_button):
		"""Update images on the screen and flip to the new screen."""			
		
		# Redraw the screen during each pass through the loop.
		screen.fill(ai_settings.bg_color)
		# Redraw all bullets behind ship and aliens.
		for bullet in bullets.sprites():
			bullet.draw_bullet()		
		#ship draw
		# alien.blitme()
		ship.blitme()
		aliens.draw(screen)

		# Draw the score information.
		sb.show_score()

		# Draw the play button if the game is inactive.
		if not stats.game_active:
			play_button.draw_button()
				
		#make the screen visible 
		pygame.display.flip()

	#fff fun_bullets
	#=========Bullets=======
	def update_bullets(self,ai_settings, screen, stats, sb, ship, aliens, bullets):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet positions.

		bullets.update()
		# Get rid of bullets that have disappeared.
		for bullet in bullets.copy():
			if bullet.rect.bottom <= 0:
				bullets.remove(bullet)
		
		self.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,aliens, bullets)		

		
	def check_bullet_alien_collisions(self,ai_settings, screen, stats, sb, ship,aliens, bullets):	
		# Check for any bullets that have hit aliens.
		# If so, get rid of the bullet and the alien.
		collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				stats.score += ai_settings.alien_points * len(aliens)
				sb.prep_score()

			self.check_high_score(stats, sb)

		if len(aliens) == 0:
			# If the entire fleet is destroyed, start a new level.
			# Destroy existing bullets and create new fleet.
			bullets.empty()
			ai_settings.increase_speed()

			# Increase level.
			stats.level += 1
			sb.prep_level()

			self.create_fleet(ai_settings, screen, ship, aliens)




	def fire_bullet(self,ai_settings, screen, ship, bullets):
		# Create a new bullet and add it to the bullets group.
		if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullets(ai_settings, screen, ship)
			bullets.add(new_bullet)	
	
	#fff fun_aliens
	#=====aliens=====

	def get_number_aliens_x(self,ai_settings, alien_width):
		"""Determine the number of aliens that fit in a row."""
		available_space_x = ai_settings.screen_Width - 2 * alien_width
		number_aliens_x = int(available_space_x / (2 * alien_width))
		return number_aliens_x	

	def get_number_rows(self,ai_settings, ship_height, alien_height):
		"""Determine the number of rows of aliens that fit on the screen."""
		available_space_y = (ai_settings.screen_Height -(3 * alien_height) - ship_height)
		number_rows = int(available_space_y / (2 * alien_height))
		return number_rows		


	def create_alien(self,ai_settings, screen, aliens, alien_number,row_number):
		"""Create an alien and place it in the row."""
		alien = Alien(ai_settings, screen)
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		aliens.add(alien)


	def create_fleet(self,ai_settings, screen, ship, aliens):
		"""Create a full fleet of aliens."""
		# Create an alien and find the number of aliens in a row.
		alien = Alien(ai_settings, screen)
		
		number_aliens_x = self.get_number_aliens_x(ai_settings, alien.rect.width)
		number_rows = self.get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
		
		# Create the fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self.create_alien(ai_settings, screen, aliens, alien_number,row_number)

	
	def ship_hit(self,ai_settings, stats, screen, ship, aliens, bullets):
		"""Respond to ship being hit by alien."""
		if stats.ships_left > 0:
			# Decrement ships_left.
			stats.ships_left -= 1
			# Empty the list of aliens and bullets.
			aliens.empty()
			bullets.empty()
			# Create a new fleet and center the ship.
			self.create_fleet(ai_settings, screen, ship, aliens)
			ship.center_ship()
			# Pause.
			sleep(0.5)
		else:
			stats.game_active = False	
			pygame.mouse.set_visible(True)	


	def check_aliens_bottom(self,ai_settings, stats, screen, ship, aliens, bullets):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = screen.get_rect()
		
		for alien in aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this the same as if the ship got hit.
				self.ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
				break	


	def update_aliens(self,ai_settings, stats, screen, ship, aliens, bullets):
		"""
		Check if the fleet is at an edge,
		and then update the postions of all aliens in the fleet.
		"""
		self.check_fleet_edges(ai_settings, aliens)
		aliens.update()
		
		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(ship, aliens):
			self.ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

		# Look for aliens hitting the bottom of the screen.
		self.check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)			

	
	def check_fleet_edges(self,ai_settings, aliens):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in aliens.sprites():
			if alien.check_edges():
				self.change_fleet_direction(ai_settings, aliens)
				break

	def change_fleet_direction(self,ai_settings, aliens):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in aliens.sprites():
			alien.rect.y += ai_settings.fleet_drop_speed 
		ai_settings.fleet_direction *= -1			

	#fff fun_score 
	#======Score==

	def check_high_score(self,stats, sb):
		"""Check to see if there's a new high score."""
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			sb.prep_high_score()







#fff run_game
def run_game():

	#initilize game and create screan
	pygame.init()
	ai_settings = Settings()

	screen = pygame.display.set_mode((ai_settings.screen_Width,ai_settings.screen_Height))
	pygame.display.set_caption("BirdsInvation")
	
	# Make the Play button.
	play_button = Button(ai_settings, screen, "Play")


	#make a ship
	ship = Ship(screen,ai_settings)
	#functions
	gf = functions()

	# Make a group to store bullets in.
	bullets = Group()

	# Make an alien.
	# alien = Alien(ai_settings, screen)
	aliens = Group()

	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)

	# Create an instance to store game statistics and create a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)



	#start a main loop
	while True:
		#watch keyboard events
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

		if stats.game_active:
			ship.update()
			# Get rid of bullets that have disappeared.
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,bullets)			
			# print(len(bullets))
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,bullets, play_button)
		


run_game()	





