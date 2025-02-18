OK - so currently all you'll have to do is run the script called "automatic.py"

This will run the multi-threaded data scraping script that dumps the values into the CSV files.

You will notice that there are some globally scoped variables at the top of the script (they are in all capital letters)
Additionally, they have rather intuitive names. They all either set input/output file names or the delays for individual functions
to avoid rate limiting (not technically legal to scrape some sites... it's kind of a gray area.)

I'm working on writing a script to join the 3 CSV files into one large one based on the steamid64s but there might be null/ 0 entries in the data when merging and I'd have to talk to you about what to do in these null/ empty cases for the format you ultimately want it to look like. 



**As a note, this will take like forever to run, so I might suggest renting a cheap cloud server or booting up a shitty old pc/ craptop to run it so that you dont have to have the main rig up and running for like 20 hours. I could (optionally create a more graphical way to see the progress because currently there is no output to show how many IDs have been processed, but I could change that if it was desired) **
