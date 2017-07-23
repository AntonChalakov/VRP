class Sidebar
{
	constructor(connection)
	{
		this.cnxn  = connection;
		this.items = [];
		this.pages = [];
		this.current_page = null;
	}

	add(page)
	{
		this.pages.push(page);
	}

	start()
	{
		for (var i = 0; i < this.pages.length; ++i) {
			var item = this.append_item_for_page(this.pages[i]);
			this.items.push(item);
		}

		this.items[0].trigger("click");
	}

	append_item_for_page(page)
	{
		var entry = $('<li></li>');

		entry.on("click", (ev) => this.select(page, ev));

		entry.load("ctrl/html/sidebar_item.html", () => {
			$(".glyphicon", entry).addClass(page.icon_class());
			$(".description", entry).html(page.title());
		});

		$("#sidebar ul").append(entry);

		return entry;
	}

	select(page, ev)
	{
		if (this.current_page != null) {
			this.current_page.close();
		}

		var c = "active";
		$(".sidebar li").removeClass(c);
		$(ev.currentTarget).addClass(c);

		page.open();

		this.current_page = page;
	}
}
