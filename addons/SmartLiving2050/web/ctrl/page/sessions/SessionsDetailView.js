class SessionsDetailView extends RoleView
{
	constructor(model, filter, selector, description_missing)
	{
		super(model, filter);

		this._selector = selector;
		this._no_desc  = description_missing;
	}

	set_tenant()
	{
		this._models[0].set_tenant();
	}

	set_technician()
	{
		this._models[0].set_technician();
	}

	set_spectator()
	{
		this._models[0].set_spectator();
	}

	kick()
	{
		this._models[0].kick();
	}

	_setup()
	{
		var desc = $('.connection', $(this._selector));
		var menu = $('.dropdown',   $(this._selector));

		menu.hide();
		menu.load("ctrl/html/sessions_dropdown.html", () => {
			var dropdown_id = "dropdown_detail"; // FIXME
			$('button.dropdown', menu).prop("id", dropdown_id);
			$('ul.dropdown-menu', menu).attr("aria-labelledby", dropdown_id);
			menu.on("click", "a.tenant",     () => this.set_tenant());
			menu.on("click", "a.technician", () => this.set_technician());
			menu.on("click", "a.spectator",  () => this.set_spectator());
			menu.on("click", "a.disconnect", () => this.kick());
			this.show();
		});
	}

	_show()
	{
		var desc = $('.connection', $(this._selector));
		var menu = $('.dropdown',   $(this._selector));

		if (this._models.length) {
			var m = this._models[0];
			desc.html("Device " + m.id());
			menu.show();
		} else {
			desc.html(this._no_desc);
			menu.hide();
		}
	}

	_close()
	{
		$(this._selector).empty();
	}
}
