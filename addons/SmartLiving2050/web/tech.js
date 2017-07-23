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

var tech = null;
var busy = null;
/**
 * Initializes objects, "start" the app.
 *
 * @author awaidler, 2016-12-16
 */
function main()
{
	var cnxn = new Connection('ws://'+location.hostname+':5500');
	var data = new HubModel(cnxn);

	tech = new TechApp(cnxn, data, busy);

	console.log("Starting app:", tech);
	tech.start();
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
			"tech/Connection.js",
			"tech/NavBar.js",
			"tech/TechApp.js",

			"tech/model/Observable.js",
			"tech/model/ClockModel.js", 
			"tech/model/DeviceModel.js",
			"tech/model/HubModel.js",
			"tech/model/ListModel.js",   
			"tech/model/SessionModel.js", 


			"tech/view/View.js",
			"tech/view/ListView.js",
			"tech/view/ClockView.js",
			
			"tech/page/Page.js",
			"tech/page/EventsDeviceListView.js",
					
			"tech/page/welcome/WelcomePage.js",
			"tech/page/welcome/WelcomeClockView.js",

					
			"tech/page/faults/FaultsPage.js",
			
			"tech/page/appointment/AppointmentPage.js",

			"tech/Notification.js",
			"tech/NotificationView.js",
			"tech/Settings.js", 					

		],
		main);

} 

loadScript("tech/Busy.js", init);
