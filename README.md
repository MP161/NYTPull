# NYTPull
This is a quick little script I wrote to complete a coding challenge given by a potential employer.
I particularly liked this challenge because it was much more similar to actual work than some other challenges I've taken on.

When this script is called, it takes a keyword argument, like 'NYTPull.py [keyword]'. The keyword is then used as a search term on the New York Times' public API.
The first five articles that come up from this search term are checked. Some relevant information is extracted from them and sent to a database.
The database operations assumes that you are using SQL, and you have a database user named 'oneSource' and they have SHOW, CREATE, DROP, and INSERT permissions.
If the database integrity is to be handled elsewhere, those permissions could be restricted to simply INSERT.
