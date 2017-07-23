class TimeCtrlPage extends PageView
{
	constructor(data_model)
	{
		super('time_control');

		this._clock = new TimeCtrlClockView(data_model);
	}

	title()
	{
		return "Time Control";
	}

	icon_class()
	{
		return "glyphicon-time";
	}

	setup()
	{
		this._clock.setup();
	}

	show()
	{
		this._clock.show();
	}

	close()
	{
		this._clock.close();
	}
}
