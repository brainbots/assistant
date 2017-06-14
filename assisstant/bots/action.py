class Action(object):
    def __init__(self, type, body, bot, keep_session):
        if (type not in ['inquiry','message'] or
            type(keep_session) is not type(True) ):
            raise ValueError(
                '__init__() is initialised by invalid attributes')
        self.type = type
        self.body = body
        self.bot = bot
        self.keep_session = keep_session
