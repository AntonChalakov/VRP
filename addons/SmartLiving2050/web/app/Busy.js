class Busy
{
	constructor()
	{
		$('#busy').load("app/html/myPleaseWait.html", () => this.show());
	}

	show()
	{
		$('#myPleaseWait').modal('show');
	}

	hide()
	{
		$('#myPleaseWait').modal('hide');
	}
}
 