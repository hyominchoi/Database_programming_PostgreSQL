Project: Swiss Tournament Database Management  - [Hyomin Choi]
===============================================================

Required Libraries and Dependencies
-----------------------------------
This project requires python v2.* and PostgreSQL.
To use PostgreSQL, we download and setup VirtualBox and Vagrant Virtual Machine. 
To run the virtual machine, type "vagrant up" and "vagrant ssh" in the terminal.

How to Run Project
------------------
* Execute tournament.sql file in PostgreSQL. 
* Execute the tournament_test.py file to run all of the unit tests, then examine the output from tournament_test.py to ensure that "Success! All tests pass!" is the last line printed in the output.
* In addition to executing tournament_test.py, one can write own python script to keep track of Swiss Tournament games. To add a player, record match results, find out current standings, import tournament.py. For more exact syntax, please look into tournament.py


Extra Credit Description
------------------------
The function swissPairings() takes care of an odd number of players. It first get the playerStandings and then find out which player hasn't gotten a free win. A free win or "bye" is given to a highest ranked player who hasn't gotten one yet.


Miscellaneous
-------------
My next goal is to include more functions in the python code.