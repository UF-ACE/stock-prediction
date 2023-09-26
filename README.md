# ACE Stock Prediction Engine
Attempts to provide a comprehensive analysis of stock behavior using two primary data channels: online sentiment and historic trends. This data is analyzed with modern machine learning techniques before giving meaningful results back to the user.

The project is split conceptually into 3 parts: sentiment analysis, trend analysis, and their union. Each of these parts will be discussed in detail below.

For general information on creating and using a custom Discord bot, see [this article](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token). These steps will need to be followed in order to interact with this project.

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

### Project Environment + Execution Instructions
To run the project, please verify the following:
- [ ] This project uses Python3. You will need to have a compatible version of Python installed in order to make + test changes.

- [ ] A list of required packages can be found in `requirements.txt`. These can be installed automatically using the following command: <br>
`pip install -r requirements.txt`

- [ ] The project requires the following 3 environment variables be added to a `.env` file in the format specified by `.env_sample`:
	- Discord bot token (see: [Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))
	- NewsAPI key (see: [NewsAPI website](https://newsapi.org/))
	- FinnHub API key (see: [FinnHub website](https://finnhub.io/))

After verifying these items, the bot can be run with the command: <br>
`python3 bot.py`

## Sentiment Analysis
