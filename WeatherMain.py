import pygame, sys, os
from pygame.locals import *
import pprint
import pywapi
import tts


class WeatherPage:

	def __init__(self, screen, clock, statusBar):
		print "weather page initialized"
		self.statusBar = statusBar
		self.running = False
		self.screen = screen

		
		self.clock = clock
		self.mainScreenOrigin = ((0,screen.get_height()/10))
		self.mainScreenSize = ((screen.get_width(), screen.get_height() - (screen.get_height()/10)))
		
		self.background = pygame.image.load(os.path.join('imgs', 'mainbackground.jpg'))
		self.background = pygame.transform.scale(self.background, (self.mainScreenSize))

		self.footer = pygame.image.load(os.path.join('imgs', 'weatherBacking.jpg'))

		
	def draw(self):
		self.screen.blit(self.background, (self.mainScreenOrigin))
		self.screen.blit(self.footer, (0,300))
	
		self.screen.blit(self.WeatherImage, (200,80))

		self.screen.blit(self.conditionWordsFont, (220,300))

		self.screen.blit(self.tempFont, (20,350))

		self.screen.blit(self.HighTempFont, (400, 350))
		self.screen.blit(self.LowTempFont, (400, 375))

		self.screen.blit(self.dayText, (100,300))
		
		
		
		
		self.statusBar.update()
		pygame.display.flip()
		
	def update(self):
		self.draw()

	def GetWeather(self):
		self.condition = self.result['forecasts'][self.day]['code']

		self.conditionWords = self.result['forecasts'][self.day]['text']
		self.conditionWordsFont = self.font.render(self.conditionWords, 1, (255,255,255))

		self.HighTemp = "High:  " + self.result['forecasts'][self.day]['high']
		self.HighTempFont = self.font.render(self.HighTemp, 1, (255,255,255))

		self.LowTemp = "Low:   " + self.result['forecasts'][self.day]['low']
		self.LowTempFont = self.font.render(self.LowTemp, 1, (255,255,255))

		self.temp = "Current Temp:  " + self.result['condition']['temp'] + "  deg"
		self.tempFont = self.font.render(self.temp, 1, (255,255,255))
		self.tempVoice = self.result['condition']['temp']

		self.whatDay = self.result['forecasts'][self.day]['day']
		self.dayText = self.font.render(self.whatDay, 1, (255,255,255))

		if 0 <= int(self.condition) <= 2:
			print 'awww shitttt'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'sad.png'))

		elif 3 <= int(self.condition) <= 12:
			print 'rainnnn'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'rain.png'))

		elif 13 <= int(self.condition) <= 16:
			print 'snow!'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'snow.png'))

		elif 17 <= int(self.condition) <= 22:
			print 'shitty'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'sad.png'))

		elif 23 <= int(self.condition) <= 25:
			print 'windyyyy burrrrrr'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'windy.png'))

		elif 26 <= int(self.condition) <= 30:
			print 'cloudsssss'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'cloudy.png'))

		elif 31 <= int(self.condition) <= 34:
			print 'niceeee'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'sun.png'))

		else:
			print 'I have a headache and want to sleep'
			self.WeatherImage = pygame.image.load(os.path.join('imgs', 'sad.png'))

		print self.condition


	#def DrawPic(self,condition):
	#	print condition
	#	if condition == 'Cloudy':
	#		print 'aint no sun out'
	#		self.WeatherImage = pygame.image.load(os.path.join('imgs', 'cloudy.png'))
	#		self.screen.blit(self.WeatherImage, (100,100))
	#		pygame.display.flip()




	
	def weatherMainLoop(self):
		while 1:
			for event in pygame.event.get():
			
			###keydown events
				if event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit()
					if event.key == K_BACKSPACE:
						self.running = False

					if event.key == K_RETURN:
						self.GetWeather()

					if event.key == K_RIGHT:
						if self.day <= 4:
							self.day += 1

						if self.day == 5:
							self.day = 0

						self.GetWeather()

					if event.key == K_LEFT:
						if self.day >= 0:
							self.day -= 1

						if self.day == -1:
							self.day = 4

						self.GetWeather()

					if event.key == K_r:
						pygame.mixer.init()
						speak = tts.Main()
						speak.getText('The current forecast is ' + self.conditionWords + '.' + ' The current temperature is ' + self.tempVoice + ' degrees.')
						pygame.mixer.music.load('everything.mp3')
						pygame.mixer.music.play()
			###

			###other events
			
			###
			
			###loop logic
			self.update()
			if not self.running:
				break
			###
			
	def begin(self):
		self.running = True
		self.day = 0

		self.font = pygame.font.Font(None,36)

		pp = pprint.PrettyPrinter(indent=4)
		self.result = pywapi.get_weather_from_yahoo('14221', 'imperial')
		pp.pprint(self.result)

		self.GetWeather()
		self.weatherMainLoop()
		
