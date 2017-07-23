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
	var cnxn = new Connection('ws://'+location.hostname+':5500'); /**'+location.hostname+'*/
	var data = new HubModel(cnxn);

	app = new MobileApp(cnxn, data, busy);

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
			"app/Connection.js",
			"app/NavBar.js",
			"app/MobileApp.js",

			"app/model/Observable.js",
			"app/model/ClockModel.js", 
			"app/model/DeviceModel.js",
			"app/model/HubModel.js",
			"app/model/ListModel.js",   
			"app/model/SessionModel.js", 
			"app/model/AppointmentModel.js",

			"app/view/View.js",
			"app/view/ListView.js",
			"app/view/ClockView.js",
			
			"app/page/Page.js",
			
			"app/page/overview/OverviewClockView.js",
			"app/page/overview/OverviewDeviceView.js",
			"app/page/overview/OverviewEventListView.js",			
			"app/page/overview/OverviewPage.js",
					
			"app/page/events/EventsDeviceListView.js",
			"app/page/events/EventsPage.js",
			
			"app/page/temperature/TemperaturePage.js",

			"app/page/energy/EnergyPage.js",

			"app/Notification.js",
			"app/NotificationView.js",
			"app/Settings.js", 

		],
		main);
} 

loadScript("app/Busy.js", init);
