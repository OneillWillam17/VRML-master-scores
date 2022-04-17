# Program revamped on 4/16/2022
I remade this project after finding out the website I was scraping released an API that allowed me to better and more consistently retrieve the data I was trying to get by webscraping. I was able to increase the effiency of the program and reduce the amount of space it used while maintaining (and improving) the readability.

# How it works
It sends a request to the VRML API, specifically the match history url, which responds with an array of the latest 200 matches played. We then iterate through those matches; checking if the division (in short, the rank of the team) is equal to 'Master' (highest rank in VRML). Once we find a match in that division, it adds the match info (overall score, team's who played, and each round score) to a message that gets sent via discord bot to a specific channel in discord. Every 10 minutes the program sends a new request and repeats the process above. 

To prevent the bot from just posting the same match info every time it sends a request: Once a match's info has been posted in discord, the matchID gets added to a list. Each time the program is run that list gets checked, and if it finds a match with the same matchID it skips over it.
