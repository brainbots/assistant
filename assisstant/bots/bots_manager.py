import settings
import importlib


class BotManager:
    def __init__(self):
        self.bots = []
        registered_bots = self.load_registered_bots()
        self.initialize_bots(registered_bots)
        self.partially_active_bot_id = None

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
        # TODO: RUN THE REQUIRED BOT
        if self.partially_active_bot_id:
            for bot in self.bots:
                if self.partially_active_bot_id == bot.id:
                    try:
                        return self.activate_bot(bot,intent)
                    except Exception as e:
                        raise(e)
        action = intent.action
        for bot in self.bots:
            if action in bot.actions:
                try:
                    return self.activate_bot(bot, intent)
                except Exception as e:
                    raise(e)
        # TODO: Raise exception if no bot can process this intent

    def activate_bot(self, bot, intent):
        bot.extract_attr(intent)
        if bot.has_missing_attr():
            try:
                self.partially_active_bot_id = bot.id
                return bot.request_missing_attr()
            except Exception as e:
                raise(e)
        else:
            try:
                print('ID is ',bot.id)
                self.partially_active_bot_id = None
                return bot.execute()
            except Exception as e:
                raise(e)
