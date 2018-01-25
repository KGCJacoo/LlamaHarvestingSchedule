# Hardware Components

* Frame/Monitor - Jacob
* Pi/Sensors/Buttons - TK
 * PIR sensor for detecting potential viewers in the room.
 * Arrow keys for navigating photos, as well as connecting to wifi for the first time.

# Software Components
 * Web GUI for user configuration - Daudi.
  * Responsible for the main user interface, via browser.
  * Keeps track of user settings, and communicates anything relevant to the cache/display code, such as image change interval, screen on-time, etc. etc.
 * Image fetching code, with modules for the various online image hosting services - Daudi
  * Based on user preferences, fetches images from an online provider and makes them available *in a generic way* to the cache/display code.
  * Maintains a database of image paths with internal UIDs.
  * Exposes an API (defined below in "Interfaces") for image requests, config updates via the hardware buttons, etc.
 * Local image caching and display - TK
  * Handles power control of the attached monitor.
  * Responds to user input on buttons, as well as the PIR sensor.
  * Keeps a local cache of images to reduce bandwidth and compute time spent on resizing.
  * Maintains an image "playlist" to allow user seeking back and forth.
  * Does readahead to allow pre-display rescaling of images to avoid lag.

# Interfaces
## IRL to Device
We talked about having 4 buttons on the pictureframe, as well as the sensor.  I'm inclined to copy known configurations from things like monitors, ie Menu, Enter, Up, Down, Left, Right. A rough initial outline:

* Menu/Enter - Enters the menu, navigable via the arrow keys.  "Enter" moves forward and selects things, "Menu" opens the menu, and once the menu is open, acts like a "back" key.
* Arrows
 Up - Tap for "upvote", AKA increasing the probability of the current picture to be shown.  Double-tap to decrease time between photos.
 Down - Tap for "downvote" the inverse of above.
 Left - Tap for the previous photo.
 Right - Tap for the next photo.
* PIR sensor - When humans are detected, activate the screen and begin displaying/rotating pictures.  The time for this ought be configurable via the web GUI.

## Image Modules to Display/Cache service
Here I'm trying to define how Daudi's and TK's code will interact.  Generally, config information is stored with the webgui code, but it can flow bidirectionally.  For example the gui can decide an initial picture delay time, but the user can override this via the hardware buttons on the pictureframe.

### Cache/Display API methods
* enable()/disable() - Should be obvious.
* setInterval(seconds) - Sets the delay time between showing photos.
* setOnTime(seconds) - Set the amount of time the display remains on after motion is detected
* ...?

### Image fetcher API methods
* getPlaylist() - Returns a list of image UIDs in the current album/account/whatever.
* getMeta(uid) - Returns metadata for an image.  Size, format, whatever else we think is important.
* getImage(uid) - Returns the actual image binary.
* ...?
