from .myEnum import Enum

DEVICE_TYPES = Enum("DEVICE_TYPES", "LIGHT RADIATOR")

MESSAGE_TYPES = Enum("MESSAGE_TYPES",
	""

	+ " GET_TIME"
	+ " SET_TIME"

	+ " GET_LOGINS"
	+ " LOGIN"
	+ " LOGOUT"
	+ " CHANGE_ROLE"
	+ " KICK"

	+ " GET_DEVICES"
	+ " ADD_DEVICE"
	+ " BREAK_DEVICE"
	+ " REPAIR_DEVICE"

	+ " EVENT"
)

ROLES = Enum("ROLES", "TENANT TECHNICIAN SPECTATOR OPERATOR")

def set_time(time):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.SET_TIME],
		'args': {
			'day':    time["day"],
			'hour':   time["hour"],
			'minute': time["minute"],
		}
	}

def kick(device_id):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.KICK],
		'args': {
			'id': device_id,
		}
	}

def add_device(dev):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.ADD_DEVICE],
		'args': {
			'id':    dev.id(),
			'type':  dev.type(),
			'state': "OK" if dev.is_ok() else "FAULT",
			'room':  str(dev.room()) # TODO
		}
	}

def break_device(dev):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.BREAK_DEVICE],
		'args': {
			'id':    dev.id(),
			'appointment': dev.get_repairAppointment()
		}
	}

def repair_device(dev):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.REPAIR_DEVICE],
		'args': {
			'id':    dev.id(),
		}
	}

def event(cause):
	return {
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.EVENT],
		'args': {
			'cause': cause
		}
	}

def event_logged_in(device_id, role):
	return event({
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.LOGIN],
		'args': {
			'id': device_id,
			'role': ROLES.toString[role]
		}
	})

def event_role_changed(device_id, role):
	return event({
		'code': MESSAGE_TYPES.toString[MESSAGE_TYPES.CHANGE_ROLE],
		'args': {
			'id': device_id,
			'role': ROLES.toString[role]
		}
	})

def event_set_time(time):
	return event(set_time(time))

def event_kicked(device_id):
	return event(kick(device_id))

def event_device_added(dev):
	return event(add_device(dev))

def event_device_broken(dev):
	return event(break_device(dev))

def event_device_repaired(dev):
	return event(repair_device(dev))
