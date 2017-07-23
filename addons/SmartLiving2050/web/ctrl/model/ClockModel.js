class ClockModel extends Observable
{
	constructor(connection)
	{
		super();

		this._cnxn = connection;

		this._local_set(0, 0, 0);
	}

	get day()
	{
		switch (this._d) {
			case 0: return "Monday";
			case 1: return "Tuesday";
			case 2: return "Wednesday";
			case 3: return "Thursday";
			case 4: return "Friday";
			case 5: return "Saturday";
			case 6: return "Sunday";
		}
	}

	get hour()
	{
		var res = this._h;
		if (res < 10) {
			res = "0" + res;
		}

		return res;
	}

	get minute()
	{
		var res = this._m;
		if (res < 10) {
			res = "0" + res;
		}

		return res;
	}

	set(d, h, m)
	{
		d = d % 7;
		h = h % 24;
		m = m % 60;

		this._cnxn.send_set_time(d, h, m);
	}

	setNextDay()     { this.set(this._d+1, this._h,   this._m); }
	setNextHour()    { this.set(this._d,   this._h+1, this._m); }
	setNextMinute()  { this.set(this._d,   this._h,   this._m+1); }

	setPrevDay()     { this.set(this._d+6, this._h,    this._m); }
	setPrevHour()    { this.set(this._d,   this._h+23, this._m); }
	setPrevMinute()  { this.set(this._d,   this._h,    this._m+59); }

	_local_set(d, h, m)
	{
		this._d = d;
		this._h = h;
		this._m = m;

		this.notify((view) => view.on_time_change(this));
	}
}
