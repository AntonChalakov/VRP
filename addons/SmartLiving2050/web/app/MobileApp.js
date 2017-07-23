class MobileApp extends ConnectionListener
{
	constructor(connection, data_model, busy)
	{
		super();

		this._cnxn = connection;
		this._data = data_model;

		this._cnxn.subscribe(this);

		this._busy = busy;

		var evdev = new EventsDeviceListView(this._data.devices());
		evdev.setup();	
		
		this._NavBar  = new NavBar(this._cnxn);
		this._NavBar.add(new OverviewPage(this._data, evdev));
		this._NavBar.add(new TemperaturePage(this._data));
		this._NavBar.add(new EventsPage(this._data, evdev));
		this._NavBar.add(new EnergyPage(this._data));
		
		this._notification = new Notification(this._data.devices());
		this._notification.setup();
		this._notification.show();

		this._settings = new Settings(this._data.sessions());
		this._settings.setup();
		this._settings.show();

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
		this._NavBar.start();
		this._busy.hide();
	}
} 
