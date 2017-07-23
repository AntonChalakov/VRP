class SessionModel extends Observable
{
	constructor(cnxn, id, role)
	{
		super();

		this._cnxn = cnxn;
		this._id   = id;
		this._role = role;
	}

	id()
	{
		return this._id;
	}

	is_tenant()
	{
		return this._role == "TENANT";
	}

	is_technician()
	{
		return this._role == "TECHNICIAN";
	}

	is_spectator()
	{
		return this._role == "SPECTATOR";
	}

	is_operator()
	{
		return this._role == "OPERATOR";
	}

	set_tenant()
	{
		this._cnxn.send_change_role_tenant(this._id);
	}

	set_technician()
	{
		this._cnxn.send_change_role_technician(this._id);
	}

	set_spectator()
	{
		this._cnxn.send_change_role_spectator(this._id);
	}

	kick()
	{
		this._cnxn.send_kick(this._id);
	}

	_local_change(role)
	{
		this._role = role;
		this.notify((view) => view.on_role_change(this));
	}

	_local_logout(role)
	{
		this.notify((view) => view.on_logout(this));
	}
}
