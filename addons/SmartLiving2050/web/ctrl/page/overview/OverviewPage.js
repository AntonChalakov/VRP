class OverviewPage extends PageView
{
	constructor(data_model)
	{
		super('overview');

		this._model = data_model;

		this._clock = new OverviewClockView(this._model.clock());
		this._devs  = new OverviewEventListView(this._model.devices());
		this._ops   = new OverviewRoleCountingView(this._model.sessions(), (s) => s.is_spectator(), '#sessions_list .spectator_count');
		this._spec  = new OverviewRoleCountingView(this._model.sessions(), (s) => s.is_operator(),  '#sessions_list .operator_count');
		this._ten   = new OverviewRoleDetailView(this._model.sessions(), (s) => s.is_tenant(),     '#sessions_list .tenant     .glyphicon');
		this._tech  = new OverviewRoleDetailView(this._model.sessions(), (s) => s.is_technician(), '#sessions_list .technician .glyphicon');
	}

	title()
	{
		return "Overview";
	}

	icon_class()
	{
		return "glyphicon-globe";
	}

	setup()
	{
		this._clock.setup();
		this._devs.setup();
		this._ops.setup();
		this._spec.setup();
		this._tech.setup();
		this._ten.setup();

	}

	show()
	{
		this._clock.show();
		this._devs.show();
		this._ops.show();
		this._spec.show();
		this._tech.show();
		this._ten.show();
	}

	close()
	{
		this._clock.close();
		this._devs.close();
		this._ops.close();
		this._spec.close();
		this._tech.close();
		this._ten.close();
	}
}
