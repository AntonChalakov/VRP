class HubModel extends Observable
{
	constructor(connection)
	{
		super();

		this._cnxn = connection;

		this._time     = new ClockModel(this._cnxn);
		this._sessions = new ListModel();
		this._devices  = new ListModel();
	} 

	open()
	{
		this._cnxn.send_get_time();
		this._cnxn.send_get_logins();
		this._cnxn.send_list_devices();
	}

	clock()
	{
		return this._time;
	}

	sessions()
	{
		return this._sessions;
	}

	devices()
	{
		return this._devices;
	}

	recv_time(d, h, m)
	{
		this._time._local_set(d, h, m);
	}

	recv_login(id, role)
	{
		this._sessions.add(new SessionModel(this._cnxn, id, role));
	}

	recv_change_role(id, role)
	{
		var sess = this._sessions.get((sess) => sess.id() == id);

		sess._local_change(role);
		this._sessions.notify((view) => view.on_role_change(sess));
	}

	recv_logout(id)
	{
		var f = (sess) => sess.id() == id;
		var sess = this._sessions.get(f);
		this._sessions.del(f);

		sess._local_logout(id);
		this._sessions.notify((view) => view.on_logout(sess));
	}

	recv_kick(id)
	{
		this.recv_logout(id); // TODO
	}

	recv_devices(dto)
	{
		this._devices.add(this._mk_dev(dto));
	}

	recv_broken(id, appointment)
	{
		var dev = this._devices.get((dev) => dev.id() == id);
		dev._local_broken(this._time, appointment);
		
		console.log("HubModel appoint: ", appointment);
		this._devices.notify((view) => view.on_device_broken(dev, this._time, appointment));
	}

	recv_repaired(id)
	{
		var dev = this._devices.get((dev) => dev.id() == id);
		dev._local_repaired();
		
		this._devices.notify((view) => view.on_device_repaired(dev, this._time));
	}

	_mk_dev(dto)
	{
		switch (dto.type) {
			case "LIGHT":    return new LightModel(this._cnxn, dto);
			case "RADIATOR": return new RadiatorModel(this._cnxn, dto);
			default:
				console.error("Device not understood:", dto);
				return null;
		}
	}
}
