class AppointmentPage extends PageView
{ 
	constructor(model, evdev)
	{
		super('appointment');

		this._devs = evdev;
	}

	title()
	{
		return "APPOINTMENTS";
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
