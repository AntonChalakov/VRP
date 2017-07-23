class RoleView
{
	constructor(model, filter)
	{
		this._model  = model;
		this._filter = filter;

		this._models = [];
	}

	setup()
	{
		this._model.register(this);
		this._setup();
	}

	show()
	{
		this._show();
	}

	close()
	{
		this._model.unregister(this);
		this._models = [];
	}

	on_add(sess)
	{
		if (!this._filter(sess)) {
			return;
		}

		this._add(sess);
	}

	on_role_change(sess)
	{
		if (this._filter(sess)) {
			/* That guy just received the proper role.
			 * In other words, he was probably ignored previously.
			 * FIXME: "probably".
			 */
			this._add(sess);
		} else {
			this._del(sess);
		}
	}

	on_logout(sess)
	{
		this._del(sess);
	}

	_add(sess)
	{
		this._models.push(sess);
		this.show();
	}

	_del(sess)
	{
		rm(this._models, sess);
		this.show();
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
