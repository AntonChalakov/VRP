class FaultsPage extends PageView
{ 
	constructor(model, evdev)
	{
		super('faults');

		this._devs = evdev;
	}

	title()
	{
		return "FAULTS";
	}

	icon_class()
	{
		return "glyphicon-wrench";
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
