class EventsPage extends PageView
{
	constructor(model)
	{
		super('events');

		this._lights = new EventsDeviceListView(model.devices());
	}

	title()
	{
		return "Events";
	}

	icon_class()
	{
		return "glyphicon-calendar";
	}

	setup()
	{
		this._lights.setup();
	}

	show()
	{
		this._lights.show();
	}

	close()
	{
		this._lights.close();
	}
}
