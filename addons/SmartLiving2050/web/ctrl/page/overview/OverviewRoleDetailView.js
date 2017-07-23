class OverviewRoleDetailView extends RoleView
{
	constructor(model, filter, selector)
	{
		super(model, filter);

		this._selector = selector;
	}

	_show()
	{
		var available = "glyphicon-ok text-success";
		var missing   = "glyphicon-remove text-danger";

		var add = this._models.length ? available : missing;
		var rem = this._models.length ? missing   : available;

		$(this._selector).addClass(add);
		$(this._selector).removeClass(rem);
	}
}
