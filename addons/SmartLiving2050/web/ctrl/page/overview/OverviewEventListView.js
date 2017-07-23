class OverviewEventListView extends ListView
{
	constructor(data_model)
	{
		super(data_model, (that, model) => new OverviewDeviceView(that, model));
	}
}
