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
			"ctrl/html/" + this.name + ".html",
			() => {
				this.setup();
				this.show();
			}
		);
	}

	title()
	{
		console.log(this, this.title);
	}

	icon_class()
	{
		console.log(this, this.icon_class);
	}

	setup()
	{
		console.log(this, this.show);
	}

	show()
	{
		console.log(this, this.show);
	}

	close()
	{
		console.log(this, this.hide);
	}
}
