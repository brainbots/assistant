class Action(object):
    def __init__(self, type, body, bot, keep_context):
        if (type not in ['inquiry','message'] or
            type(keep_context) is not type(True) ):
            raise ValueError(
                '__init__() is initialised by invalid attributes')
        self.type = type
        self.body = body
        self.bot = bot
        self.keep_context = keep_context
