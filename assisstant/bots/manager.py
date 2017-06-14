import settings
import importlib


class BotManager:
	def __init__(self):
		self.bots = []
		registered_bots = self.load_registered_bots()
		self.initialize_bots(registered_bots)

	def load_registered_bots(self):
		registered_bots = settings.REGISTERED_BOTS
		bots = []
		for bot in registered_bots:
			*module, classname = bot.split(".")
			bots.append((".".join(module), classname))
		return bots

	def initialize_bots(self, bots):
		id = 0
		for module, classname in bots:
			module = importlib.import_module(module)
			bot_class = getattr(module, classname)
			self.bots.append(bot_class(id))
			id += 1

	def run_action(self, intent):
		action = intent.action
		for bot in self.bots:
			if action in bot.actions:
				if bot.validate_intent(intent):
					try:
						return bot.execute(intent)
					except Exception as e:
						raise(e)
		# TODO: Raise exception if no bot can process this intent
