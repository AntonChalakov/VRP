/**
 * "Interface" used by Connection to dispatch received messages as method
 * calls.
 *
 * @author Andreas Waidler <andreas.waidler@student.kit.edu>
 */
class ConnectionListener
{
	recv_time()       { }
	recv_login()      { }
	recv_devices()    { }
	recv_change_role(){ }
	recv_logout()     { }
	recv_kick()       { }
	recv_broken()     { }
	recv_repaired()   { }
}

/**
 * Implements the protocol (sending and receiving) and dispatches messages to
 * registered ConnectionListener instances.
 *
 * @author Andreas Waidler <andreas.waidler@student.kit.edu>
 */
class Connection
{
	constructor(url)
	{
		this._url = url;
		this._h = [];
		this._id = null;
	}

	open(on_open)
	{
		this._sck = new WebSocket(this._url);
		this._sck.onopen     = on_open;
		this._sck.onmessage  = (msg) => this._onMessage(msg);
		this._sck.onclose    = (err) => this._onClose(err);
		this._sck.onerror    = (err) => this._onError(err);
	}

	subscribe(h)
	{
		this._h.push(h);
	}

	send_login()
	{
		this._send({
			code: "LOGIN",
			args: {
				role: "TENANT"
			}
		});
	}

	send_get_time()
	{
		this._send({
			code: "GET_TIME",
			args: { }
		});
	}

	send_set_time(d, h, m)
	{
		this._send({
			code: "SET_TIME",
			args: {
				day: d,
				hour: h,
				minute: m,
			}
		});
	}

	send_get_logins()
	{
		this._send({
			code: "GET_LOGINS",
			args: { }
		});
	}

	send_change_role_tenant(id)
	{
		this._send_change_role(id, "TENANT");
	}

	send_change_role_technician(id)
	{
		this._send_change_role(id, "TECHNICIAN");
	}

	send_change_role_spectator(id)
	{
		this._send_change_role(id, "SPECTATOR");
	}

	send_kick(id)
	{
		this._send({
			code: "KICK",
			args: {
				id: id,
			}
		});
	}

	send_list_devices()
	{
		this._send({
			code: "GET_DEVICES",
			args: { }
		});
	}

	send_broken_light(light_id)
	{
		this._send_broken("LIGHT", light_id);
	}

	send_repaired_light(light_id)
	{
		this._send_repaired("LIGHT", light_id);
	}

	send_broken_radiator(id)
	{
		this._send_broken("RADIATOR", id);
	}

	send_repaired_radiator(id)
	{
		this._send_repaired("RADIATOR", id);
	}


	_onMessage(MessageEvent)
	{
		var m = JSON.parse(MessageEvent.data);

		console.log("Event", MessageEvent, "parsed to", m);

		if (m.code != "EVENT") {
			console.log("Ignoring non-event code.");
			return;
		}

		var code = m.args.cause.code;
		var args = m.args.cause.args;
		this._h.forEach(this._message_dispatcher(code, args));
	}

	_message_dispatcher(code, args)
	{
		switch (code) {
			case "LOGIN":
				if (this._id == null) 
				{
					this._id = args.id;
				}
				return (h) => h.recv_login(args.id, args.role);   

			case "CHANGE_ROLE":
				return (h) => h.recv_change_role(args.id, args.role);

			case "LOGOUT":
				return (h) => h.recv_logout(args.id);

			case "KICK":
				return (h) => h.recv_kick(args.id);

			case "SET_TIME":
				return (h) => h.recv_time(args.day, args.hour, args.minute);

			case "ADD_DEVICE":
				return (h) => h.recv_devices(args);

			case "BREAK_DEVICE":
				console.log("args in Connection:", args);
				return (h) => h.recv_broken(args.id, args.appointment);

			case "REPAIR_DEVICE":
				return (h) => h.recv_repaired(args.id);

			default:
				console.error("Message not understood:", m);
		}
	}

	_onClose(e)
	{
		console.log(this._onClose, e);
	}

	_onError(e)
	{
		console.log(this._onError, e);
	}

	_send_change_role(id, role)
	{
		this._send({
			code: "CHANGE_ROLE",
			args: {
				id: id,
				role: role,
			}
		});
	}

	_send_broken(type, id)
	{
		this._send({
			code: "BREAK_DEVICE",
			args: {
				id: id,
				type: type
			}
		});
	}

	_send_repaired(type, id)
	{
		this._send({
			code: "REPAIR_DEVICE",
			args: {
				id: id,
				type: type
			}
		});
	}

	_send(message_object)
	{
		console.log("Sending message:", message_object);
		this._sck.send(JSON.stringify(message_object));
	}
}
