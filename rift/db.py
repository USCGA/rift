import mongoengine

print("[i] Connecting to database.")

def connection(debug=False):
	if debug:
		connection = mongoengine.connect('rift', host='localhost')
	else:
		connection = mongoengine.connect('rift', host='mongo')


