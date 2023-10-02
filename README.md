# ACE Stock Prediction Engine

The ACE Stock Prediction Engine is a comprehensive stock analysis tool that leverages online sentiment analysis and historical trends. This open-source project is split into three key components: sentiment analysis, trend analysis, and their integration. This readme aims to provide clear instructions for setting up and using the project effectively.

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
   - [Using Git](#using-git)
   - [Project Environment + Execution Instructions](#project-environment-execution-instructions)
3. [Contributing](#contributing)
4. [License](#license)
5. [Acknowledgments](#acknowledgments)
6. [Screenshots](#screenshots)
7. [FAQ](#faq)
8. [Version History](#version-history)
9. [Contact](#contact)
10. [Security](#security)

## Overview

The ACE Stock Prediction Engine combines sentiment analysis and historical data to provide valuable insights into stock behavior. It assists users in making informed investment decisions.

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

### Contributing
We welcome contributions! Follow these steps to contribute:

- Fork the repository.
- Create a new branch: git checkout -b yourname-branchname
- Make your changes, commit, and push.
- Submit a pull request to the original repository.
- License
- This project is licensed under the LICENSE_NAME License.

### Acknowledgments
We acknowledge the creators of the third-party libraries and APIs that power this project.

### Screenshots
(Add relevant screenshots or visual aids here.)

### FAQ
(Include common questions and their solutions, if any.)

### Version History
(Keep a changelog to document updates, bug fixes, and new features.)

### Contact
(Provide contact information or links to community forums.)

### Security
(Include security considerations or best practices, if applicable.)
## Sentiment Analysis
