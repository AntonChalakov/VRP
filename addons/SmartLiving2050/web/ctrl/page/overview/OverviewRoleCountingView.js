class OverviewRoleCountingView extends RoleView
{
	constructor(model, filter, selector)
	{
		super(model, filter);

		this._selector = selector;
	}

	_show()
	{
		$(this._selector).html(this._models.length);
	}
}
