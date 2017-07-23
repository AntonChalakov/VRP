class TimeCtrlClockView extends ClockView
{
	constructor(clock)
	{
		super(clock);
	}

	_setup()
	{
		$('#timecontrol .day    .add').on('click', () => this._model.setNextDay());
		$('#timecontrol .hour   .add').on('click', () => this._model.setNextHour());
		$('#timecontrol .minute .add').on('click', () => this._model.setNextMinute());
		$('#timecontrol .day    .sub').on('click', () => this._model.setPrevDay());
		$('#timecontrol .hour   .sub').on('click', () => this._model.setPrevHour());
		$('#timecontrol .minute .sub').on('click', () => this._model.setPrevMinute());
	}

	_show()
	{
		var d = this._model.day;
		var h = this._model.hour;
		var m = this._model.minute

		$('#timecontrol .day    .active').html(d);
		$('#timecontrol .hour   .active').html(h);
		$('#timecontrol .minute .active').html(m);
	}
}
