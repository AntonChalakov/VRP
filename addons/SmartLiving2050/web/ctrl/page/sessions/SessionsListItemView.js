class SessionListItemView extends View
{
	constructor(parent_view, model)
	{
		super(model);
		this._parent = parent_view;
		this._view = null;
	}

	on_role_change(sess)
	{
		this.show();
	}

	on_logout()
	{
		this.close();
	}

	_setup()
	{
		/* Stolen from http://www.w3schools.com/jsref/met_table_insertrow.asp
		 *   -- awaidler, 2016-12-15
		 */
		var table = $('#sessions-table')[0]
		var row   = table.insertRow(0);
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var menu = row.insertCell(2);

		menu.className = "dropdown";

		menu = $(menu);
		menu.load("ctrl/html/sessions_dropdown.html", () => {
			var m = this._model; // FIXME
			var dropdown_id = "dropdown_" + m.id();
			$('button.dropdown', menu).prop("id", dropdown_id);
			$('ul.dropdown-menu', menu).attr("aria-labelledby", dropdown_id);
			menu.on("click", "a.tenant",     () => m.set_tenant());
			menu.on("click", "a.technician", () => m.set_technician());
			menu.on("click", "a.spectator",  () => m.set_spectator());
			menu.on("click", "a.disconnect", () => m.kick());
			menu.show();
		});

		this._view = $(row);
	}

	_show()
	{
		var td = $("td", this._view);
		td[0].innerHTML = this._model.id();
		td[1].innerHTML = this._model._role;
	}

	_close()
	{
		this._view.remove()
		this._parent.remove(this);
	}
}
