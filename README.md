# Job Application Bot

  

A Python script that automates the job application process

  

## Table of Contents

  

- [Introduction](#introduction)

- [Features](#features)

- [Requirements](#requirements)

- [Installation](#installation)

- [Usage](#usage)

- [Disclaimer](#Disclaimer)

  

## Introduction

  

This script uses Playwright to automate the job application process on Dice. It logs in to your account, performs a job search, and applies to multiple jobs automatically. It is designed to save you time and effort when job hunting on Dice.

  

## Features

  

- Log in to Dice with your credentials.

- Search for jobs using specific keywords.

- Apply to multiple jobs with just one script run.

- Customizable user-agent to mimic different web browsers.

  

## Requirements

  

- Python 3.x

- [Playwright](https://playwright.dev) (installed automatically via pip)

- [Chromium browser](https://playwright.dev/docs/browsers#install-chromium) (automatically downloaded by Playwright)

  

## Installation

  

1. Clone this repository:   
   ```
   git clone https://github.com/Sameerakhatoon/AutomateJobApplication.git
   cd AutomateJobApplication
   ```

2. Install the required Python libraries:
```
pip install playwright
```

3. Install Chromium browser (required by Playwright):
```
Chromium browser (automatically installed by Playwright)
```
  

## Usage

1. Open the script (`AutomateDice.py`) and fill in your Dice.com login credentials:
    `email = "your_email@example.com" password = "your_password"`
    
2. Customize the search keywords and user-agent as needed:
    `search_keywords = '".net developer"'  # Keywords for the search custom_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.288 Mobile Safari/537.36"`
    
3. Run the script:    
    `python AutomateDice.py`
    
4. The script will log in, perform the job search, and automatically apply to multiple jobs. It will save job titles to a file named `job_titles.txt`.


## Disclaimer

This script is intended for educational and personal use only. Use it responsibly and adhere to ethical standards when automating interactions with websites.
