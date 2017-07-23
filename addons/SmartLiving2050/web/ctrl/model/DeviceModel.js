class DeviceModel extends Observable
{
	constructor(connection, dto)
	{
		super();

		this._dto = dto;
		this._cnxn = connection;
	}

	id()
	{
		return this._dto.id;
	}

	type()
	{
		return this._dto.type;
	}

	room()
	{
		return this._dto.room;
	}

	state()
	{
		return this._dto.state;
	}

	is_ok()
	{
		return this.state() == "OK";
	}

	_local_broken()
	{
		this._dto.state = "FAULT";
		this.notify((view) => view.on_device_broken(this));
	}

	_local_repaired()
	{
		this._dto.state = "OK";
		this.notify((view) => view.on_device_repaired(this));
	}
}

class LightModel extends DeviceModel
{
	constructor(connection, dto)
	{
		super(connection, dto);
	}

	break_device()
	{
		this._cnxn.send_broken_light(this.id());
	}

	repair_device()
	{
		this._cnxn.send_repaired_light(this.id());
	}

	desc()
	{
		return this.is_ok()
			? this.id() + " in " + this.room() + " works."
			: this.id() + " in " + this.room() + " broken.";
	}
}

class RadiatorModel extends DeviceModel
{
	constructor(connection, dto)
	{
		super(connection, dto);
	}

	break_device()
	{
		this._cnxn.send_broken_radiator(this.id());
	}

	repair_device()
	{
		this._cnxn.send_repaired_radiator(this.id());
	}

	desc()
	{
		return this.is_ok()
			? this.id() + " in " + this.room() + " works."
			: this.id() + " in " + this.room() + " broken.";
	}
}
