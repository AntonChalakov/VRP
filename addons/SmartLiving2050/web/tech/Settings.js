class Settings extends View
{
	constructor(model)
	{
		super(model);
		
		this._list = model;
		this._session = null;
	}

	on_add(model)
	{
		if (this._session != null) {
			return;
		}
		
		this._session = model;
		this._session.register(this);
		this._list.unregister(this);
		
		this.show();
	}
	
	on_role_change(model)
	{
			alert("YOUR ROLE CHANGED");
			//MODAL und dann wieder zurück auf index oder auf die entsprechendne Seite (aber dann mit neuer SessionID) TODO 
	}
	
	on_logout(model)
	{
			console.log("LOGGED OUT");
			window.location = "index.html";	
	}
	
	_setup() {

		$('#navbar-settings').on('click', () => 
			{
				$('#mySettings').modal('show');
			});
		
		$('#settings-language').on('click', () => 
			{
				alert("TODO: Change language");
			});
		
		$('#settings-disconnect').on('click', () => 
			{
				this._session.kick();
			});
	}
	
	_show()
	{
		console.log("this._session in SETTINGS.js" + this._session);
		
		if (this._session == null) {
			$('#settings_id').html("-");
			$('#settings_status').html("NOT LOGGED IN");

		} else {
			$('#settings_id').html(this._session.id());
			$('#settings_status').html("LOGGED IN");
		}
	}
}
