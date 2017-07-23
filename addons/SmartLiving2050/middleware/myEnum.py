# Python before version 3.4 did not have enums. This is a hack, based on:
# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
#   -- awaidler, 2016-11-23
def enum_hack(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)

	if 'iteritems' in enums:
		toString   = dict((value, key) for key, value in enums.iteritems())
		fromString = dict((key, value) for key, value in enums.iteritems())
	else:
		toString   = dict((value, key) for key, value in enums.items())
		fromString = dict((key, value) for key, value in enums.items())

	enums['toString'] = toString
	enums['fromString'] = fromString
	return type('Enum', (), enums)

# Make the hack above compatible with PEP435
# (new Python version that actually supports enums).
#    -- awaidler, 2016-12-10
def Enum(name, elements):
	return enum_hack(*(elements.split()))
