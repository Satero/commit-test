# Github API Commit History

Given the name of a repo and the username of its owner, I used Github's API to:
* Determine the weekday with the greatest average of commits over the past year or given timeline.
* Sort the weekdays by their respective averages of commits over the past year or given timeline.


## Assumptions Made For This Project
1. I'm given the name of a repository, but I'm also given the username of its owner, which appears to be required for many/all of the APIs dealing with repositories and commits.
2. The timeline a person is restricted to requesting is up to 1 year.
3. I define a year as specifically 52 weeks.

## Third-Party Packages Used
* requests - Sends HTTP requests to the Github API
* calendar - Translated the output date of the Github API, in ISO 8601, to the desired format.
* argparse - Built the CLI UX to allow for different user inputs and flags.
* sys - Retrieved user arguments from the command line.
* unittest - Created unittests for the project.


## Instructions to Use
Using Python 3, basic usage is as follows:
python (or python3, depending on which OS is being used) commit_history.py <name of repo> <repo owner's username>

To change the number of weeks in the past we're looking at (where default = 52 weeks):
python commit_history.py <name of repo> <repo owner's username> -weeks=48

To view the list of weekdays with their commit averages and change sorting order from its default, descending order 'desc' to 'asc':
python commit_history.py <name of repo> <repo owner's username> -useList=True -sort='asc'

To run the unittests (empty output = passed):
python commit_history.py <name of repo> <repo owner's username> -runTests=True


## Thoughts, Notes, Comments
When looking through the Github API docs, it appeared that many/all of the APIs dealing with repositories and commits also required the name of the owner, which is why I assumed that I was also being given that.

It was convenient that Github API had a section specifically to output the commit averages of the weekdays over the past year - all I needed to do was sum the lists for each week, then sort the list of totals, average them and retrieve the max average for the primary objective. Splicing the list of weeks retrieved from the API helped me achieve the first bonus objective, and changing how I sorted the list of totals helped me achieve the second bonus objective.

At first, I assumed that a person could look at any length of timeline in the history of commits of the given repository, so when I first saw the Statistics API, I didn't want to use that solution since I was limited to the span of a year. I saw that the Commits API had a possible solution that was not limited by time, but I learned that it only returned up to 30 commits. In the end, I ended up using the Github Statistics API anyways.

I'm not sure how Github API interacts with a leap year, so I went with the assumption that a year was 52 weeks in length.


## Future Adaptations
Even though the Commits API is limited to 30 commits in length, I think it's certainly possible to write a function that is able to loop through the whole commit history of a repo, because possible parameters include "since" and "until" as timeline limiters in ISO 8601 format. The function would start from the beginning of the repo's history, output the first 30 commits, retrieve the date of the last commit, and then recall the Commits API with that date in the "since" parameter - and then it would repeat until no commits remained. In this way, the given problem we are dealing with would not be limited by 52 weeks. Not only that, but we would also be able to define the specific timeline we would want to look at the history of, between two dates we would want to look at. However, it gives each commit's timestamp in ISO 8601, so we would have to loop through every commit, convert its date into a weekday, and then add it to a running total based on whichever weekday it was, which would make the runtime linear as opposed to the current solution's constant runtime.

Given all the information in the JSON that the Commits API returns, compared to the Statistics API, we'd be able to do the following:
* Take the average over a different timeline - e.g. the month with the greatest average of commits over the past 10 years.
* Figure out which message or substring was the most common in a commit.
* Figure out who commited the most in a specific timeline.
etc.

I think it's cool that there's a lot of ways we could go with this project!


## Author
* Justin Picar