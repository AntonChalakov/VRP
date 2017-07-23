class OverviewEventListView extends ListView
{
	constructor(data_model)
	{
		super(data_model, (that, model) => new OverviewDeviceView(that, model));
	}

	on_device_broken(dev)
	{
	}

	on_device_repaired(dev)
	{
	}
}
