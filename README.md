![Example of Plot Output](http://parking.joshuakatz.me/njit/past-7-days.png)

# Don't send your kids to college. There's no parking!

NJIT has no parking.

That's incorrect. It does have parking lots but they're just 
overpriced ($375/semester and rising) and far too low capacity. 
Unfortunately the people who run NJIT are too greedy to cough up 
a few of the dollars we bleed ourselves of to give us somewhere 
to park. My carpool group and I, for the past few years, have 
found ourselves ariving hours earlier than our classes start time 
just to have any hope of find parking. 

The scripts in this repository are used to evaulate the parking 
situation at NJIT. I started this for a few reasons.

## Reason the first

I don't want to arive 3 hours before a class and sit in 
uncomfortable chairs doing nothing. This project generates useful 
plots that help me and my friends plan when we should show up if 
we want a hope of finding parking.

## Reason the second

Many people I have talked to about the parking situation have 
been brainwashed into thinking that it would be impossible to 
solve. They say things like "They should just sell guaranteed 
spots" or "It's impossible to predict how many spots you'd need 
and when you'd need them". This is just false. In my plots you 
can see at what times NJIT's parking decks are over saturated 
with cars. From this data we can answer simple qustions. One 
question I had originaly sought to answer was about NJIT's rented 
overflow lot. NJIT has purchesed exclusive access to a series of 
parking lots next to the school. These lots are opened at noon 
every day (Monday through Saturday as I understand). They have a 
set of guards who stand outside of the lot for the whole day. 
From my plots I can tell you that their noon every day policy is 
stupid. On Friday the overflow lot is unnecessary. On Tuesday and 
Thursday their overflow lot should open at 10:30AM to 11AM. On 
Wednesday I belive the noon-open policy would be fine. 


# Decisions

Part of this is in PHP, Python 2, and Python 3. These scripts are 
running on multiple <1GB of ram VMs I have and communicate with 
unix pipes across SSH (ssh remote_server_one "php -f 
/some/script.php | gzip" | gunzip). This is not ideal but it 
works and will likely work for some time. The data collection was 
hacked together in an hour. The plot took an afternoon.

For these plots I've used Viridis because it is a very good color 
bar for RG color blind people. If you're another kind of color 
blind I'd suggest you choose another color bar. Viridis is a good 
choice in general because it is linearly responsive.

If I was going to change these plots at all I'd change them to be 
on a finer timescale (say 5 minutes instead of 5 hour) so you can 
see more fine grain effects in the changes.

# Further Work

I need to look at other factors. These plots are generated with a 
lot of averaging because this data set can only give me an 
approximate number of available spots. I've binned all data by 
weekday and hour because if one person leaves the parking deck 
and someone else (1 minute later) parks in the parking lot then 
there wasn't really a space "available". Averaging like I'm doing 
smooths out the data and makes it tell the story I want to tell: 
"How hard will it be to find parking". I might write some code to 
use google maps to tell me how long it would take to drive along 
each road that surounds the school and train some kind of ML 
classification model to be able to detect (My ranking 1 to 10 of 
the expeirance, from # of remaining spaces, time of day, day of 
week, time it takes to drive along each road, etc) if it is a 
good idea to be ariving at a specific time.

Maybe I could write an app that collects this data from multiple 
students and uses all of it to build a finer picture of how bad 
NJIT's parking really is.
