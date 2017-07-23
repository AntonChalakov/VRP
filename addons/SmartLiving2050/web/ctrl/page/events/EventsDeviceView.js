class EventsDeviceView extends View
{
	constructor(parent_view, device_model, selector)
	{
		super(device_model);

		this._parent = parent_view;
		this._selector = selector;

		this._html = null;
	}

	on_device_broken()
	{
		this.show();
	}

	on_device_repaired()
	{
		this.show();
	}

	_setup()
	{
		this._html = $('<li></li>');
		this._html.prop("id", this._model.id());
		this._html.load("ctrl/html/events_item.html", () => this.show());
		this._html.on("click", "button", (ev) => this._clicked(ev));

		$(this._selector).append(this._html);
	}

	_show()
	{
		var classes_ok    = "btn-success active";
		var classes_fault = "btn-danger active";

		var button_ok    = $('button.sctrl-ok', this._html);
		var button_fault = $('button.sctrl-fault', this._html);

		button_ok.removeClass(classes_ok);
		button_fault.removeClass(classes_fault);

		if (this._model.is_ok()) {
			button_ok.addClass(classes_ok);
		} else {
			button_fault.addClass(classes_fault);
		}

		// var desc = l.room + " (" + l.id + ")";
		$('.description', this._html).html(this._model.desc());
	}

	_clicked(ev)
	{
		var clicked_ok    = $(ev.target).hasClass("sctrl-ok");
		var clicked_fault = $(ev.target).hasClass("sctrl-fault");
		var is_ok = this._model.is_ok();

		if (clicked_ok && !is_ok) {
			this._model.repair_device();
		} else if (clicked_fault && is_ok) {
			this._model.break_device();
		} else {
			console.error("ERROR! Something weird was clicked.", ev);
		}
	}
}
