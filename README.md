
# dash - billboard

This is a dashboard for visualization of test results of a continous
delivery pipeline, optimized for large monitors that can be set up
in a team working place.

It builds on the [CI Dashboard by Pingworks](https://github.com/pingworks/dash).
A configured setup is required for dash billboard to work.

In addition to the optimized display there is function to shoot the
developer responsible for the failure using a toy USB rocket launcher.

## Screenshot

![CI Dashboard Screenshot](https://raw.github.com/seibert-media/dash-billboard/public/screenshots/screenshot.png "Screenshot")

## Recommended Equipment

*german version*

* [Raspberry PI](http://www.amazon.de/s/url=search-alias%3Daps&field-keywords=Raspberry+Pi+Mod.+B+Rev+2.0)
* [Raspberry PI case](http://www.amazon.de/s/url=search-alias%3Dcomputers&field-keywords=Raspberry%20Pi%20Geh%C3%A4use%20-%20bel%C3%BCftet)
* [Power supply](http://www.amazon.de/s/url=search-alias%3Daps&field-keywords=Steckernetzteil%20f%C3%BCr%20Raspberry%20Pi)
* [Passive cooling for raspberry](http://www.amazon.de/s/url=search-alias%3Delectronics&field-keywords=K%C3%BChlk%C3%B6rper%20f%C3%BCr%20den%20Raspberry%20Pi)
* [USB rocket launcher "Thunder"](http://www.amazon.de/s/url=search-alias%3Daps&field-keywords=USB%20Raketenwerfer%20%22Thunder%22) (USB ID 0a81:0701 Chesen Electronics Corp. USB Missile Launcher)
* Monitor with HDMI connector or adapter

## Setup

[Raspbian (wheezy)](http://www.raspbian.org/) is highly recommended as operating system for the pi.

Specify the URL of your dash setup in `rocket/Config.py` and `display/js/dashbord.js`. Calibrate the position of your developers in `Config.py`.

Use the following scripts on your rpi to set up the dashboard. After that, the
raspberry pi should start the dashboard automatically in a browser
after boot and shut itself down when the browser window is closed.

```bash
$ cd deploy
$ ./setup_display
$ ./setup_rocket
$ dash-billboard
```

## Development

Same origin policy has to be deactivated to use the dashboard, you can use the following command to do that.

Chrome:

> $ chrome --disable-web-security --allow-file-access-from-files display/index.html

## License

Copyright 2013 //SEIBERT/MEDIA GmbH

Author: Ingmar Drewing <idrewing@seibert-media.net>
        Benjamin Peter <bpeter@seibert-media.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

