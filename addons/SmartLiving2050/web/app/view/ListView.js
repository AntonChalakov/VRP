class ListView extends View
{
	constructor(model, item_factory)
	{
		super(model);
		this._views = [];
		this._factory = item_factory;

	}

	setup()
	{
		super.setup(); // Calls on_add() for each model that already exists.
	}

	show()
	{
		super.show();
		this._views.forEach((v) => v.show());
	}

	close()
	{
		super.close();
		this._views.forEach((v) => v.close());
		this._views = [];
	}

	on_add(model)
	{
		var view = this._factory(this, model)
		view.setup();
		view.show();

		this._views.push(view);
	}

	remove(view)
	{
		rm(this._views, view);
	}
}
