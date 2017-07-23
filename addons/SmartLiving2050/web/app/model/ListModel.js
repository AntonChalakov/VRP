class ListModel extends Observable
{
	constructor()
	{
		super();

		this._models = [];
	}

	register(view)
	{
		super.register(view);

		this._models.forEach((model) => view.on_add(model));
	}

	add(model)
	{
		this._models.push(model);

		this.notify((view) => view.on_add(model));
	}

	get(filter)
	{
		var hits = this._models.filter(filter);

		if (hits.length != 1) {
			console.error("Expected exactly one hit: Looking for", filter, "in", this._models, "resulted in", hits);
			return null;
		}

		return hits[0];
	}

	del(f)
	{
		this._models.filter(f).forEach((h) => rm(this._models, h));
	}
}
