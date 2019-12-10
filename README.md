# 507Project
Final project for SI 507

For my final project I decided to make a web app that easily allows users to compare a university's football and basketball school to make it easy to determine which schools should be considered "basketball" schools and which should be considered "football" schools.

Data sources used for this project:
For this project, I scraped data from four differnet websites to gather information on a schools basketball team and football team. From these sources I gathered information including winning percentage, offensive rating, defensive rating, recruiting class, school logo, and location. I also used the opencage api to get coordinates for the schools for mapping features in my app. To gather this data, simply run the final_project.py file and the data will be gathered. 

Data processing:
Since I was only able to scrape rankings of a team's characteristics, I needed to process the data by using my add_better() function to add labels to schools determining if they are  a "football" or "basketball" school.

I also needed to add state abbreviations for some of my graphing capabilities, however the abbreviations were not availabe from the api I used, I only got back the full state name. To get the abbreviations, I used a dictionary with the state names as keys and abbreviations as values to populate the abbreviation column of my locations df.

I also needed to separate my data by year to give users the option to search in specific years, so another large processing step I needed was to make separate dfs separated by year. Additionally, I needed to create a df with avearges to give the user the option to look at a more historical representation of the data. To do this I combined my main df to find the average of all my features per team before separating into my yearly dfs.

User guide:
To run my program, simply run the final_project.py file which will scrape the data and populate my database. After this you will run the app.py file and enter the link returned into your browser so you will be able to interact with the program
