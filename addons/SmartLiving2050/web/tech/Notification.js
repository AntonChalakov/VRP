class Notification extends ListView
{
	constructor(model)
	{
		super(model, (that, model) => new NotificationView(that, model));$
	}
	
	on_device_broken()
	{
	}
	
	on_device_repaired()
	{
	}
}
