class OverviewPage extends PageView
{ 
	constructor(data_model, evdev)
	{
		super('overview');
		
		this._model = data_model;
		this._devs = evdev;


		this._clock = new OverviewClockView(this._model.clock());
	}

	title()
	{
		return "OVERVIEW";
	}

	icon_class()
	{
		return "glyphicon-globe";
	}

	setup()
	{
		this._clock.setup();
	}

	show()
	{
		this._clock.show();
		this._devs.show();	
	}

	close()
	{
		this._clock.close();
	}
} 
