class EventsPage extends PageView
{ 
	constructor(model, evdev)
	{
		super('events');

		this._devs = evdev;
	}

	title()
	{
		return "EVENTS";
	}

	icon_class()
	{
		return "glyphicon-calendar";
	}

	setup()
	{
	}

	show()
	{
		this._devs.show();
	}

	close()
	{
	}
	
} 
