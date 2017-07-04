from .abstract_bot import AbstractBot
from bots.action import Action
from urllib.request import urlopen
from pprint import pprint
import json
import settings

class WeatherBot(AbstractBot):
	def __init__(self, id):
	    actions = ['weather']
	    super().__init__(id, actions)
	    #REQUIRED
	    self.city = None
	    self.country = None
	    #OPTIONAL
	    self.datetime = None
	    self.unit = None

	def extract_attr(self, intent):
	    if not intent.parameters.get('address'):
	        return

	    addr = intent.parameters['address']

	    if not self.city:
	       if (type(intent.parameters['address']) is dict and
	          (intent.parameters['address'].get('city') or
	           intent.parameters['address'].get('admin-area'))):
	           self.city = next(city for city in
	               [addr.get('city'),addr.get('admin-area')] if city is not None)

	    if not self.country:
	       if (type(intent.parameters['address']) is dict and
	           intent.parameters['address'].get('country')):
	           self.country = addr.get('country')

	def request_missing_attr(self):
	    if not self.city:
	        return Action(
		        action_type = 'inquiry',
		        body = 'Please specify the city.\n',
		        bot = self.id,
		        keep_context = True)

	    if not self.country:
	        return Action(
		        action_type = 'inquiry',
		        body = 'Please specify the country.\n',
		        bot = self.id,
		        keep_context = True)

	def is_long_running(self):
	    return False

	def has_missing_attr(self):
	    return (self.country == None or self.city == None)

	def execute(self):
	    # self.datetime = address.get('datetime')
	    # self.unit = address.get('unit')
	    try:
	    	CLIENT_ID = settings.WEATHER_CLIENT_ID
	    	CLIENT_SECRET = settings.WEATHER_CLIENT_SECRET
	    	request = urlopen('https://api.aerisapi.com/observations/{},{}?client_id={} & client_secret={}'
	    	    .format(self.city,self.country,CLIENT_ID,CLIENT_SECRET))

	    	# & fields=ob.tempC,ob.weather,ob.icon
	    	response = request.read()
	    	jso = json.loads(response)
	    	weather_forecast = ''
	    	if jso['success']:
	    	    ob = jso['response']['ob']
	    	    weather_forecast = 'The current weather in {}, {} is {} with a temperature of {}°C.'.format(
	    	        self.city, self.country, ob['weather'].lower(), ob['tempC'])
	    	else:
	    	    print ("An error occurred: %s" % (jso['error']['description']))
	    	    self.clear()
	    	    return Action(
	    	        action_type = 'inquiry',
	    	        body = '- Invalid city-country pair.\n'
	    	            '- Please specify the city.',
	    	        bot = self.id,
	    	        keep_context=True
	    	        )
	    	request.close()
	    	self.clear()
	    	return Action(
		        action_type = 'message',
			    body = weather_forecast,
			    bot = self.id,
			    keep_context = False)
	    except Exception as e:
	        self.clear()
	        raise(e)

	def clear(self):
	  self.city = None
	  self.country = None
