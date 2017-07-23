class Busy
{
	constructor()
	{
		// $('#busy').load("ctrl/html/myPleaseWait.html", () => this.show());
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
