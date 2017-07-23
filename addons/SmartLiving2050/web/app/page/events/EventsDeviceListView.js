class EventsDeviceListView extends View
{
	constructor(model)
	{
		super(model);
		this._current_list = [];
		this._upcoming_list= [];
	}
	
	on_add()
	{
	}

	on_device_broken(dev, time, appointment)
	{
 		this._add_to_current_list(dev, time, appointment, 'glyphicon-warning-sign');
		this._add_to_upcoming_list(dev, time, appointment, 'glyphicon-wrench');
	}
	
	on_device_repaired(dev, time)
	{
		var noappointment = null; 
		this._add_to_current_list(dev, time, noappointment, 'glyphicon-ok');
	}

	_setup()
	{
	}

	_show()
	{
		var l = $("#insert_current");
		var l2 = $("#insert_current_overview");
		var l3 = $("#insert_upcoming");
		
		if (this._current_list.length > 0) 
		{
			l.empty();
			l2.empty();
		}
				
		this._current_list.forEach((li) => l.prepend(li));
		this._current_list.forEach((li) => l2.prepend(li));
		this._upcoming_list.forEach((li) => l3.prepend(li));
	}

	_add_to_current_list(dev, time, appointment, icon)
	{	
		var icon = $('<span class="glyphicon ' + icon + '"></span>');
		var desc = $('<span></span>');
		var timelabel = $('<span></span>');
		var entry = $('<li class="list-group-item"></li>');

		desc.html('&nbsp;' + dev.desc());
		timelabel.html('&nbsp;(' + time.day.substring(0,3) + ',&nbsp;' + time.hour + ':' + time.minute + ')');

		entry.append(icon); 
		entry.append(desc);
		entry.append(timelabel);

		this._current_list.push(entry);
		this.show();
	}
	
	_add_to_upcoming_list(dev, time, appointment, icon)
	{
		var icon = $('<span class="glyphicon ' + icon + '"></span>');
		var text = $('<span></span>');
		var entry = $('<li class="list-group-item"></li>');
			
		var appoint_day = "";
		var appoint_start = "";
		var appoint_end = "";
		var appoint = [];
		
		appoint_day = this._get_day(appointment[0]);
		
 		appoint_start = this._get_hour(appointment[1][0]);
 		appoint_start += ":";
 		appoint_start += this._get_hour(appointment[1][1]);
		
 		appoint_end = this._get_hour(appointment[2][0]);
 		appoint_end += ":";
 		appoint_end += this._get_hour(appointment[2][1]);	


		
		
		text.html('&nbsp;Technician Appointment (' + appoint_day + ', ' + appoint_start + ' - ' + appoint_end + ')');

		entry.append(icon); 
		entry.append(text);

		this._upcoming_list.push(entry);
		this.show();
	}
	
	
 	_get_day(day)
 	{
 		switch (day) {
 			case 0: return "Mon";
 			case 1: return "Tue";
 			case 2: return "Wed";
 			case 3: return "Thu";
 			case 4: return "Fri";
 			case 5: return "Sat";
 			case 6: return "Sun";
 		}
 	}

	_get_hour(hour)
 	{
 		var res = hour;
 		if (res < 10) {
 			res = "0" + res;
 		}

 		return res;
 	}
}
