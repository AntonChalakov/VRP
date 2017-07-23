class Busy
{
	constructor()
	{
		$('#busy').load("tech/html/myPleaseWait.html", () => this.show());
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
 