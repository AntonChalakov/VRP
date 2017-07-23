class EventsDeviceListView extends ListView
{
	constructor(model)
	{
		super(model, (that, model) => this._mk_view(that, model));
	}

	on_device_broken(dev)
	{
	}

	on_device_repaired(dev)
	{
	}

	_mk_view(that, model)
	{
		switch (model.type()) { // TODO: OOP
			case "LIGHT":    return new EventsDeviceView(that, model, '#lights');
			case "RADIATOR": return new EventsDeviceView(that, model, '#radiators');
			default:
				console.error("No device view for model:", model);
				return null;
		}
	}
}
