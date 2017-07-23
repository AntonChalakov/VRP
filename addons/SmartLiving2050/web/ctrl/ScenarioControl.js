class ScenarioControl extends ConnectionListener
{
	constructor(connection, data_model, busy)
	{
		super();

		this._cnxn = connection;
		this._data = data_model;

		this._cnxn.subscribe(this);

		this._busy = busy;

		this._navbar  = new NavBar(this._cnxn);
		this._sidebar = new Sidebar(this._cnxn);

		this._sidebar.add(new OverviewPage(this._data));
		this._sidebar.add(new TimeCtrlPage(this._data.clock()));
		this._sidebar.add(new SessionsPage(this._data));
		this._sidebar.add(new EventsPage(this._data));

		this._logged_in = false;
	}

	start()
	{
		this._busy.show();

		this._cnxn.open(() => this.login());
	}

	login()
	{
		this._cnxn.send_login();
	}

	recv_login()
	{
		if (this._logged_in) {
			return;
		}
		this._logged_in = true;

		this._cnxn.subscribe(this._data);

		this._data.open();
		this._sidebar.start();
		this._busy.hide();
	}
}
