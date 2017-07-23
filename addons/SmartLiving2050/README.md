## Gruppe 1


# Smart Living 2050
Für unser Projekt verwenden wir die Versionsverwaltung [git](https://git-scm.com/), für die 3D-Modellierung [Blender](https://www.blender.org/). Die VR-Umgebung in der wir hauptsächlich entwickeln heißt [PolyVR](https://github.com/Victor-Haefner/polyvr) und ist unter Ubuntu und Derivaten lauffähig. Die BPM Modellierung wird mit Microsoft Visio realisiert, was ihr euch über den [SCC-Zugang](https://www.scc.kit.edu/dienste/9312.php) zu Microsoft Imagine herunterladen könnt.

Die drei verlinkten Programme sind gut dokumentiert und es sind zahlreiche Tutorials dazu im Internet zu finden. Insbesondere falls es Fragen zu oder Probleme mit git und Ubuntu gibt, wendet euch an den Informatiker eures Vertrauens.



## Group 3 (Interaction) ##

Group 3 implements interaction between virtual and physical worlds.
The virtual world is modeled and developed by other teams in PolyVR.
We visualize the virtual world in a CAVE with a Flystick 2.
Regarding the physical world, we target any device in that is capable of
running a modern web browser that supports web applications,
such as smartphones, tablets, and personal computers.

### Project Structure ###

PolyVR allows for easy realization of software interfaces
between virtual and physical worlds.
To create interfaces, we create Python scripts within PolyVR
and configure appropriate input devices/events for the individual scripts.
As devices/events, we primarily use Flystick 2 and WebSockets.
Furthermore, we use computer mouse and keyboard for testing purposes
outside of the CAVE.

All scripts we add to PolyVR are merely entry points
that dispatch to the actual event handling code
that resides as regular Python files in the project directory.
That way, we ensure maintainability and modularity
of our Python middleware.
While PolyVR runs only Python2, our middleware is compatible with
both Python2 and Python3.5.

We implement the web application front-end
by leveraging the Bootstrap framework.
Using Bootstrap allows us to create a beautiful and responsive design.
The front-end uses JavaScript to communicate with the middleware over WebSockets.
When a project is running in PolyVR, PolyVR runs a web server at port 5500.
Files and sub-directories (?) in the project's root directory
are available at http://localhost:5500/{file\_name}.
Note that nothing has to be configured for this feature.
Thus, we do not add any HTML/CSS/JS files to PolyVR.
Keeping files out of PolyVR reduces maintainenance overhead
and allows the front-end to be tested without a running PolyVR instance.

### Testing ###

The middleware includes regular Python unit tests
which can be launched, for example, by invoking `py.test`.
Furthermore, modularity allows us to test front-end independently
from the middleware and vice-versa.

To test the front-end,
open the main HTML file in your browser (via file://{path/to/file}).
To test and debug communication of the front-end.
you can start a WebSocket command line server,
e.g. [wscat](https://www.npmjs.com/package/wscat) by running `wscat --listen 5500`
and fake a running middleware instance.
Vice-versa, you can use `wscat` to test a running middleware instance
by invoking `wscat --connect localhost:5500`.

The Python middleware can be run independently from PolyVR.
`LocalMiddlewareServer.py` implements a stand-alone Python3 websocket server
based on the
[websockets](http://websockets.readthedocs.io/en/stable/index.html)
library.
