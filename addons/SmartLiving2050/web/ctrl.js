/**
 * Load a script from the provided URL and run a callback
 * once it's loaded and executed.
 *
 * Borrowed from http://stackoverflow.com/questions/950087/how-do-i-include-a-javascript-file-in-another-javascript-file/950146#950146
 */
function loadScript(url, callback)
{
	// Adding the script tag to the head as suggested before
	var head = document.getElementsByTagName('head')[0];
	var script = document.createElement('script');
	script.type = 'text/javascript';
	script.src = url;

	// Then bind the event to the callback function.
	// There are several events for cross browser compatibility.
	script.onreadystatechange = callback;
	script.onload = callback;

	// Fire the loading
	head.appendChild(script);
}

/**
 * Load a list of scripts via URLs sequentially and run a callback afterwards.
 *
 * @author awaidler, 2016-12-16
 * @author awaidler, 2016-12-23
 */
function loadScripts(scripts, callback)
{
	if (scripts.length) {
		loadScript(scripts.shift(), () => loadScripts(scripts, callback));
	} else {
		callback();
	}
}

var app = null;
var busy = null;
/**
 * Initializes objects, "start" the app.
 *
 * @author awaidler, 2016-12-16
 */
function main()
{
	var host = location.hostname != "" ? location.hostname : "localhost";
	var cnxn = new Connection('ws://'+ host +':5500'); /**'+location.hostname+'*/
	var data = new HubModel(cnxn);

	app = new ScenarioControl(cnxn, data, busy);

	console.log("Starting app:", app);
	app.start();
}


/**
 * Helper function that removes the first occurrence of an element from the
 * supplied array.
 *
 * @author Andreas Waidler <andreas.waidler@student.kit.edu>
 */
function rm(arr, elem)
{
	var i = $.inArray(elem, arr);
	if (i >= 0) {
		arr.splice(i, 1);
	}
}



/* Run main() once all other scripts have been loaded.
 *
 * Order is important, otherwise we get undefined class/reference errors.
 *
 *   -- awaidler, 2016-12-16
 */

function init()
{
	busy = new Busy();
	busy.show();
	loadScripts(
		[
			"ctrl/Connection.js",
			"ctrl/NavBar.js",
			"ctrl/ScenarioControl.js",
			"ctrl/Sidebar.js",

			"ctrl/model/Observable.js",
			"ctrl/model/ClockModel.js",
			"ctrl/model/DeviceModel.js",
			"ctrl/model/HubModel.js",
			"ctrl/model/ListModel.js",
			"ctrl/model/SessionModel.js",

			"ctrl/view/View.js",
			"ctrl/view/ListView.js",
			"ctrl/view/RoleView.js",
			"ctrl/view/ClockView.js",

			"ctrl/page/Page.js",

			"ctrl/page/events/EventsDeviceListView.js",
			"ctrl/page/events/EventsDeviceView.js",
			"ctrl/page/events/EventsPage.js",

			"ctrl/page/overview/OverviewClockView.js",
			"ctrl/page/overview/OverviewDeviceView.js",
			"ctrl/page/overview/OverviewEventListView.js",
			"ctrl/page/overview/OverviewPage.js",
			"ctrl/page/overview/OverviewRoleCountingView.js",
			"ctrl/page/overview/OverviewRoleDetailView.js",

			"ctrl/page/sessions/SessionsDetailView.js",
			"ctrl/page/sessions/SessionsListItemView.js",
			"ctrl/page/sessions/SessionsListView.js",
			"ctrl/page/sessions/SessionsPage.js",

			"ctrl/page/time_control/TimeCtrlClockView.js",
			"ctrl/page/time_control/TimeCtrlPage.js",
		],
		main);
}

loadScript("ctrl/Busy.js", init);
