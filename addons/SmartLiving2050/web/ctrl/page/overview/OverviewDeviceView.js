class OverviewDeviceView extends View
{
	constructor(parent_view, device_model)
	{
		super(device_model);

		this._view = null;
		this._changed = false;
	}

	on_device_broken()
	{
		this._changed = true;
		this.show();
	}

	on_device_repaired()
	{
		this._changed = true;
		this.show();
	}

	_show()
	{
		/* Initially, hide good devices. */
		if (!(!(this._model.is_ok()) || this._changed)) {
			console.log("Ignoring good device", this);
			return;
		}

		if (this._view != null) {
			this._view.remove();
		}

		this._view = this._model.is_ok()
		           ? this._mk_ev_view_repaired(this._model)
		           : this._mk_ev_view_broken(this._model);

		$("#events_list").prepend(this._view);
	}

	_close()
	{
		this._changed = false;

		if (this._view != null) {
			this._view.remove();
		}
	}

	_mk_ev_view_broken(dev)
	{
		return this._mk_ev_view(dev, "glyphicon-alert text-danger");
	}

	_mk_ev_view_repaired(dev)
	{
		return this._mk_ev_view(dev, "glyphicon-ok text-success");
	}

	_mk_ev_view(dev, icon)
	{
		var v = $('<li></li>');
		v.load("ctrl/html/overview_event.html", () => {
			v.addClass("lead");
			$(".glyphicon", v).addClass(icon);
			$(".description", v).html(dev.desc());
		});

		return v;
	}
}
