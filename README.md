Fitbit Tools
============

This is a small set of scripts used to talk with Fitbit devices.
Communication is done via the USB dongle, not via direct Bluetooth Low
Energy.

This is mainly intended for people wanting to hack on the Fitbit, not
those who want something useful for syncing with the Fitbit servers! For
that you should look at the galileo project:

https://bitbucket.org/benallard/galileo

Requirements
------------

Construct:

https://github.com/construct/construct

Hidapi and cython-hidapi:

https://github.com/trezor/cython-hidapi

If you are on OS X, you will also want the following patch to hidapi,
which makes it possible to distinguish between two USB endpoints that
present the same identifying information:

https://github.com/signal11/hidapi/issues/193
