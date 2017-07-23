class EventsDeviceListView extends View
{
	constructor(model)
	{
		super(model);
		this._faults_list = [];
		this._appoint_list= [];
	}
	
	on_add()
	{
	}

	on_device_broken(dev, time, appointment)
	{
 		this._add_to_faults_list(dev, time, appointment, 'glyphicon-warning-sign');
		this._add_to_appoint_list(dev, time, appointment, 'glyphicon-wrench');
	}
	
	on_device_repaired(dev, time)
	{
		var noappointment = null; 
		this._add_to_faults_list(dev, time, noappointment, 'glyphicon-ok');
	}

	_setup()
	{
	}

	_show()
	{
		var l = $("#overview_faults");
		var l2 = $("#faults_insert_current");
		var l3 = $("#overview_appointments");
		var l4 = $("#appointment_insert_current");
		
		if (this._faults_list.length > 0) 
		{
			l.empty();
			l2.empty();
		}
		
		if (this._appoint_list.length > 0) 
		{
			l3.empty();
			l4.empty();
		}
				
		this._faults_list.forEach((li) => l.prepend(li));
		this._faults_list.forEach((li) => l2.prepend(li));
		this._appoint_list.forEach((li) => l3.prepend(li));
		this._appoint_list.forEach((li) => l4.prepend(li));

	}

	_add_to_faults_list(dev, time, appointment, icon)
	{	
		var icon = $('<span class="glyphicon ' + icon + '"></span>');
		var desc = $('<span></span>');
		var timelabel = $('<span></span>');
		var entry = $('<li class="list-group-item"></li>');

		desc.html('&nbsp;[Kuthsweg 45, Apt. 12]:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + dev.desc());
		timelabel.html('&nbsp;(' + time.day.substring(0,3) + ',&nbsp;' + time.hour + ':' + time.minute + ')');

		entry.append(icon); 
		entry.append(desc);
		entry.append(timelabel);

		this._faults_list.push(entry);
		this.show();
	}
	
	_add_to_appoint_list(dev, time, appointment, icon)
	{
		var icon = $('<span class="glyphicon ' + icon + '"></span>');
		var text = $('<span></span>');
		var timelabel = $('<span></span>');
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


		text.html('&nbsp;[' + appoint_day + ', ' + appoint_start + ' - ' + appoint_end + '] Kuthsweg 45, Apt. 12:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + dev.desc());
		timelabel.html('&nbsp;(' + time.day.substring(0,3) + ',&nbsp;' + time.hour + ':' + time.minute + ')');

		entry.append(icon); 
		entry.append(text);
		entry.append(timelabel);

		this._appoint_list.push(entry);
		this.show();
	}
	
	
 	_get_day(day)
 	{
 		switch (day) {
 			case 0: return "Monday";
 			case 1: return "Tuesday";
 			case 2: return "Wednesday";
 			case 3: return "Thursday";
 			case 4: return "Friday";
 			case 5: return "Saturday";
 			case 6: return "Sunday";
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
