class ClockView extends View
{
	constructor(clock)
	{
		super(clock);
	}

	on_time_change(clock)
	{
		this.show();
	}
}
