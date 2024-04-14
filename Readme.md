Student Name: Srivanth Purusothaman

Student ID: 20031609

Mail ID: 20031609@mydbs.ie


# FOOTBALL LEAGUE-TAGBLE DATA PIPELINE
# Project Overview:

This project attempts to scrape English Premier League standings data from a certain website, save the collected data in a MongoDB database, and make the data available via a REST API endpoint. The primary components include site scraping, data preparation, MongoDB storage, API endpoint, and cron-based automated updates.

Scraped Data      --> EPL.py(main file)
Delete Database   --> mongoDrop.py

# Key Features:

1.   Web Scraping:

* The script uses the requests library to retrieve HTML material from a specific website holding EPL standings.
* BeautifulSoup, a parsing package, is used to traverse and retrieve the necessary table data from the downloaded HTML.
* It uses class names like "Table__TableWrapper-r2czfk-3 hezlIo" and "Table__TableRow-r2czfk-8 dwCAtX" to target the specific table container and rows that include standings data.

2.   Data Preprocessing:

* Before being put in the database, the extracted data is cleaned up a bit.

      * .strip() removes leading and trailing spaces from text.
      * .replace(' ', '_') replaces spaces in headers with underscores (_),   
        potentially resulting in better user-friendly column names and easier database processing.
      * Headers are converted to lowercase using.lower() to ensure uniformity.
      * .replace(',', '') is used to remove commas (,) from prospective numeric 
        data (for example, points, goals).
      * Attempts to convert the cleaned data to float values with the try... 
        except block. If conversion fails (non-numeric data), the data is stored as a string to avoid problems.
  
3.   MongoDB Storage:

* The cleaned and processed data is saved in a MongoDB database called "EPLLeague".
* The EPL standings information is stored in a database collection titled "standings".
* The functions mongodb_Connection(), insert_Data(), and fetch_Data() help you communicate with the MongoDB database:

      * connect() makes a connection to the MongoDB instance.
      * insert() takes the scraped and processed data and stores it in the 
        "" collection of the "EPLLeague" database.
      * get() extracts data from the "standings" collection and 
        returns it for further use.
4. Dropping a Database

* Permanently deletes a specific database from MongoDB
* This drop_db() function deletes the provided database, in this case "EPLLeague"

4.   API Endpoint:

* The project uses Flask, a web framework, to establish a RESTful API endpoint accessible by a specified URL (e.g., /api/leagueStandings/db).
* When a user makes a request to this endpoint, the script fetches the most recent EPL standings data from the MongoDB database using fetch_Data.
* The retrieved data is then transformed to JSON format with jsonify.
* Finally, the JSON-formatted data is returned in response to the API call. This enables other apps to simply connect and utilize EPL standings data.

5.    Cron Job Scheduling (Optional):
      
* The information provided indicates that the script is set to execute on Fridays using crontab, a job scheduler in Unix-like systems. This suggests that the data is scraped and updated in the database on a weekly schedule.
* You may want to alter the cron schedule based on how frequently you want to keep the data updated.
