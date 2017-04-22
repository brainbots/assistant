class Intent(object):
	def __init__(self, action, score, params, query, timestamp, **kwargs):
		self.action = action
		if score > 1 or score < 0:
			raise ValueError("__init__() got invalid score value '%d', score should be between 0 and 1." % score)
		self.score = score
		self.parameters = params
		self.query_string = query
		self.timestamp = timestamp

		allowed_args = ('metadata', 'contexts')
		for k, v in kwargs.items():
			if k in allowed_args:
				setattr(self, k, v)
			else:
				raise TypeError("__init__() got an unexpected keyword argument '%s'" % k)
