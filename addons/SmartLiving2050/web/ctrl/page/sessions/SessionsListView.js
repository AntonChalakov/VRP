class SessionsListView extends ListView
{
	constructor(model)
	{
		super(model, (that, model) => new SessionListItemView(that, model));
	}

	on_role_change()
	{
	}

	on_logout()
	{
	}
}
