# IVY-HOMES-ASSESSMENT
## Problem Statement
The task involves developing a website data extracting script to extract information
about the top 20 movies listed under each genre on IMDb, as well as their latest 10
user reviews. The goal is to gather comprehensive data for a broad analysis of
movie trends and reception across various genres.

## Solution
I have implemented a solution using Python, utilizing web scraping techniques to extract data from the IMDb website. The extracted data is then parsed and stored in a SQLite database using SQLAlchemy for efficient management and future use.

## Setup Instructions
### Prerequisites
- Python 3.x installed

### Installation
- clone this repository into your system
  ```bash
     git clone https://github.com/adityaa22/IVY-HOMES-ASSESSMENT.git
     ```
### Setup Virtual Enviornment in project Folder
- open Terminal in the project directory and run the command:
     ```bash
     python -m venv venv
     ```
- activate the venv
  ```bash
    source venv/bin/activate
    ```
  THe virtual enviornment has been succesfully created and activated ( use ```deactivate``` command to deactivate the virtual enviornment)

### Install dependencies
- To install the dependencies run commad:
```bash
  pip install -r requirements.txt
  ```
- This will install all the required deoendencies for the project. This project uses ```beautifulSoup``` module from ```bs4``` library for websrapping, ```SQLAlchemy``` as an ORM,  ```sqlite``` as database and ```requests``` module to make request to the webpage.

## Execution
- Open a terminal in the project folder
- make sure that the virtual enviornment is active
- run the following command in the root folder of project:
  ```Bash
    python -m scripts.main
    ```
- This will trigger the execution of script and the script will take some time to run as it searches multiple webpages for extracting data
- A new file ```imdb.db``` will be created which will have binary data of our database, this can be viewed using applications like ```DB Browser for SQLite```

## Important Considerations
- As per the requirements of problem statement , need for dynamic javascript rendering was not needed (The list of movies for each  genre wer 50 on initial load and list of reviews wer 25). However this canbe easily solved using ```selenium``` library to trigger necessary javascripts before scrapping
- The script relies on structure of IMDB site and if it changes in future, the script will have to be updated for web scrapping modules of script
- I have made use of multi_threading to scrape movies at same time to optimise the script.
- I have taken max_workers to be 8 and to each thread I have provided a list of genre to extract from.
- For database queries only insert dunctions are mentioned as of now.TO run the script it is recommended to delete the existing ````imdb.db```` file and then run the script for accurate results

- ## Database Decription
  ### architecture
  ![alt text](https://github.com/adityaa22/IVY-HOMES-ASSESSMENT/blob/main/DB_dump/DB_arch.png)

  (P.S. - "rank" attribute was removed from movies table)

  ## Script Explaination
  * (This section will be updated in future)
  
  * (The script is well structured and commented, can refer to it for explaination for now)
