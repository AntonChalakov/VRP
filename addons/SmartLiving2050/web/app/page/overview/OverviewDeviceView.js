class OverviewDeviceView extends View
{
	constructor(parent_view, device_model, selector)
	{
		super(device_model);

		this._parent = parent_view;
		this._selector = selector;
	}

	on_device_broken()
	{
 		this._add_to_list('glyphicon-warning-sign');
	}

	on_device_repaired()
	{
 		this._add_to_list('glyphicon-ok');
	}

	_setup()
	{
	}

	_show()
	{
	}

	_add_to_list(icon)
	{
		var icon = $('<span class="glyphicon ' + icon + '"></span>');
		var desc = $('<span></span>');
		var entry = $('<li class="list-group-item"></li>');

		desc.html('&nbsp;' + this._model.desc());

		entry.append(icon);
		entry.append(desc);

		$("#insert_current_overview").prepend(entry);

		this.show();
		
		$("#empty_current_overview").addClass("hidden");	
	}
}
