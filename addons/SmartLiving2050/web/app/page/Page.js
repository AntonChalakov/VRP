/**
 * Basic HTML page in the dashboard.
 *
 * @author Andreas Waidler <andreas.waidler@student.kit.edu>
 */ 
class PageView
{
	constructor(name)
	{
		this.name = name;

	}

	open()
	{
		$('#dashboard').load(
			"app/html/" + this.name + ".html",
			() => {
				this.setup();
				this.show();
			}
		);
	}

	title()
	{
	}

	icon_class()
	{
	}

	setup()
	{
	}

	show()
	{
	}

	close()
	{
	}
}
