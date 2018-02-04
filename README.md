# reddit-scraper
A small python program i made, that scrapes images off of subreddits (only imgur and redd.it links though).

It currently has two modes:
  1. Manual input - Start in manual input with -manual keyword. You have to enter subreddit, maxmimum downloads, how the 
    submissions are sorted(hot, top_day, top_hour..., controversial and new), username and password, in that order. 
      
  2. Input via config.ini - Default mode. Reads all info from the config.ini file(needs to be in the same folder as the program)
  
 The reddit app's public- and secret ID and where to save the images is always read from the config.ini file.
