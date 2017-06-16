from .abstract_bot import AbstractBot
from bots.action import Action
class WeatherBot(AbstractBot):
	def __init__(self, id):
	    actions = ['weather']
	    super().__init__(id, actions)
	    #REQUIRED
	    self.city = None
	    #OPTIONAL
	    self.country = None
	    self.datetime = None
	    self.unit = None

	def validate_intent(self, intent):
	    if (type(intent.parameters['address']) is dict and
	       intent.parameters['address'].get('city')):
		    return True
	    return False

	def request_missing_attr(self,intent):
	    return Action(
		    action_type = 'inquiry',
		    body = 'Please specify the city',
		    bot = self.id,
		    keep_context = True)

	def execute(self, intent):
	    address = intent.parameters['address']
	    self.city = address.get('city')
	    self.country = address.get('country')
	    self.datetime = address.get('datetime')
	    self.unit = address.get('unit')
	    try:
		#TODO: Use a Weather API , Don't forget to clear the params
		    weather_forecast = 'Temp is 35 C'
		    return Action(
		        action_type = 'message',
			    body = weather_forecast,
			    bot = self.id,
			    keep_context = False)
	    except Exception as e:
            # Raise the exception e
                raise(e)

