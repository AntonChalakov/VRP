class NotificationView extends View
{
	constructor(parent_view, device_model)
	{
		super(device_model);

		this._parent = parent_view;
	}

	on_device_broken(dev, time, appointment)
	{
		var content = "";
		content += '[Kuthsweg 45, Apt. 12]: ';
		content += dev.desc();
		content += ".<br><br>An appointment has been scheduled on ";
		
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
						
		content += appoint_day;
		content += " between ";
		content += appoint_start;
		content += " and ";
		content += appoint_end; 
		content += ".";
		
		$('#myNotification').modal('show');
		$('#notification_desc').html(content);
		
				
	}

	on_device_repaired()
	{
		$('#myNotification').modal('hide');
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
