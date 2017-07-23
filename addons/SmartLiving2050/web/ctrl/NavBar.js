function restart_sc()
{
	/*TODO*/
	alert("Restart // TODO");

}

function language_english()
{
	/*TODO*/
	alert("Change to English // TODO");
}

function language_german()
{
	/*TODO*/
	alert("Change to German // TODO");
}

class NavBar
{
	constructor(connection)
	{
		this.cnxn = connection;
		$('#navbar').load('ctrl/html/navbar.html', function() {
		});
	}
}
