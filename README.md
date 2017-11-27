# OtterShare
Attempting to create my own screenshot sharing program to replace what I've been using for years.

Notes about the program thus far and some details.
The images are saved as a png, and can be told to upload the image to imgur, after the upload is done the url is copied to your clipboard. The url and delete hash is then saved to a local text file for
future usages.


The Config.py contains all the configurable variables, and saves itself as an ini in the cwd.

Some notes on the Config.
client_id: This is an id given to you by imgur for uploading images, to get your own you must register the application with imgur. Without one the uploading will fail.
save_hotkey: This suppose multiple key presses, but only alt, ctrl, shift, and a through z work with it currently.

That's all there is for now to worry about.