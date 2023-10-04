# ACE Stock Prediction Engine
Attempts to provide a comprehensive analysis of stock behavior using two primary data channels: online sentiment and historic trends. This data is analyzed with modern machine learning techniques before giving meaningful results back to the user.

Below you will find descriptions and usages of supported commands, as well as a brief explanation of how those commands are implemented "behind-the-scenes."

This project uses [this template](https://github.com/jaARke/discord-lambda-py) for creating a serverless Discord bot using Python. Review the instructions in the template's README (specifically, the "Development" section) for some useful background.

## Getting Started
### Using Git
You'll first need to fork this repository. Then, to clone the fork to your local machine, use the following command: <br>
`git clone https://github.com/your-username/forked-repository.git`

Once done, you'll want to add the original repo as an upstream target: <br>
`git remote add upstream https://github.com/UF-ACE/stock-prediction.git`

To sync the forked repo with changes in the original, use the following command: <br>
`git pull upstream/branch-name`
Where branch-name is the name of a branch in the original repo. Note that this pulls branch-name's remote changes into the branch of the fork you currently have checked out.

To submit changes to the original repo, follow the steps below:
- Navigate to the fork on your local machine
	- `cd forked-repo`
- Create a new branch for your changes
	- `git checkout -b yourname-branchname`
- ...make changes...
- Commit and push your changes
	- `git commit -m "..."`
	- `git push --set-upstream origin yourname-branchname`
- Submit a pull request -> be sure to select the correct base branch in the original repo

### Project Environment + Contributing
This project uses Python 3.9. You can download the latest version of Python [here](https://www.python.org/downloads/).

Additional commands should be added to files in the `/commands` directory. Reference the template linked above for more information on command function structure.

Helper functions harnessed by commands should be added to `/utils`. These functions should be unit tested.

Given the nature of this project, it is difficult to test new functionality locally. Changes made are only reflected in our bot when those changes are pushed to the `master` branch of this repo. That being said, ensure the following before submitting a pull request:
 - [ ] All new command functionality is thoroughly unit tested. Discord-specific context aside, this will ensure that a function you've created produces the expected output for a given input. This is especially important for functions that rely on external data sources, such as the stock market API.
 - [ ] All new command functionality is documented in the `README.md` file. This includes a description of the command, its usage, and any other relevant information.
 - [ ] All command requirements are noted in the `requirements.txt` file. This includes any new packages that need to be installed for the command to work.
 - [ ] All relevant API keys are noted in `.env_sample`, `README`, and described in the notes of the pull request. This will ensure these variables can be added to the production environment when the time comes.

 ### API Keys
Below is a list of the APIs that this project uses. Local data retrieval (execution of some of the functions in `/utils`) will require that keys for these API are specified in a `.env` file on your local machine.
- [Finnhub](https://finnhub.io/)
- [News API](https://newsapi.org/)


## Sentiment Analysis
### Overview
Sentiment analysis involves mapping a user's query to a valid stock ticker, collecting headlines related to that stock, and analyzing the sentiment of those headlines. The sentiment analysis is performed using the [VADER](https://github.com/cjhutto/vaderSentiment) library, which is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. The analysis returns a compound sentiment score, which is a value in the range [-1, 1] that represents the overall sentiment of the text. A score of -1 indicates extremely negative sentiment, while a score of 1 indicates extremely positive sentiment.

News headlines are collected from FinnHub, News API, Google News, and Yahoo Finance.
### Commands
#### `/sentiment [type] [company] [interval]`
- **Description:** Collects and (optionally) analyzes sentiment data for a given stock ticker over a given time interval.
- **Usage:**
	- `[type]` is one of `collect` or `analyze`, and specifies whether the commands should (only) collect data or run an analysis
	- `[company]` is a valid stock ticker or company name
	- `[interval]` is an integer in the range [1, 30] and specifies the number of days of data to collect
- **Returns:** A total number of headlines collected, and three sample headlines. If the `analyze` option is specified, the command will also return a sentiment analysis of the collected headlines. The user will be warned if the command fails to find more than 25 headlines.