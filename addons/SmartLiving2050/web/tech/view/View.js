class View
{
	constructor(model)
	{
		this._model = model;
	}

	setup()
	{
		this._model.register(this);

		this._setup(); // Delegate to child class.
	}

	show()
	{
		this._show(); // Delegate to child class.
	}

	close()
	{
		this._model.unregister(this);

		this._close(); // Delegate to child class.
	}

	_setup()
	{
	}

	_show()
	{
	}

	_close()
	{
	}
}
