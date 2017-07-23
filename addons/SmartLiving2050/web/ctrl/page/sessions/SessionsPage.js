class SessionsPage extends PageView
{
	constructor(model)
	{
		super('sessions');

		this._model = model;

		this._tenant        = new SessionsDetailView(this._model.sessions(), (s) => s.is_tenant(),     '#tenant', "No tenant logged in.");
		this._technician    = new SessionsDetailView(this._model.sessions(), (s) => s.is_technician(), '#technician', "No technician logged in.");
		this._sessions_list = new SessionsListView(this._model.sessions());
	}

	title()
	{
		return "Sessions";
	}

	icon_class()
	{
		return "glyphicon-user";
	}

	setup()
	{
		this._tenant.setup();
		this._technician.setup();
		this._sessions_list.setup();
	}

	show()
	{
		this._tenant.show();
		this._technician.show();
		this._sessions_list.show();
	}

	close()
	{
		this._tenant.close();
		this._technician.close();
		this._sessions_list.close();
	}
}
