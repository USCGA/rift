import mongoengine

print("[i] Connecting to database.")
connection = mongoengine.connect('rift', host='mongo')

