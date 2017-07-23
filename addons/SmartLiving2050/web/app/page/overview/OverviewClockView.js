class OverviewClockView extends ClockView
{
	constructor(clock)
	{
		super(clock);
	}

	_show()
	{
		var d = this._model.day;
		var h = this._model.hour;
		var m = this._model.minute

		$('#time_overview').html(d + ", " + h + ":" + m);
	}
}
