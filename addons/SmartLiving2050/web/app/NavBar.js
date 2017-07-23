class NavBar
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
		var entry = $('<li class="col-xs-3 text-center app-navbar-box1"></li>');

		entry.on("click", (ev) => this.select(page, ev));

		entry.load("app/html/navbar_item.html", () => {
			$(".glyphicon", entry).addClass(page.icon_class());
			$(".description", entry).html(page.title());
		});

		$("#navbar ul").append(entry);

		return entry;
	}

	select(page, ev)
	{
		if (this.current_page != null) {
			this.current_page.close();
		}

		var c = "app-navbar-active";
		$("#navbar li").removeClass(c);	
		$(ev.currentTarget).addClass(c);

		page.open();

		this.current_page = page;
	}	
} 
