# Sigma-Terminal: A finance research and portfolio management terminal
© Stanglmeier 2021

# Short Description: 
Sigma Terminal is the best tool for retail investors to research, analyze and optimize stocks and other digital assets. On the one hand, Sigma aims to display and distribute basic and advanced information on every stock and digital asset listed on the NYSE, NASDAQ or similar. On the other hand, Signal uses Artificial Intelligence and Machine Learning to give MVP Portfolio recommendations, news media and social media sentiment analysis, as well as community-selected stocks.

# Core Services: 
Sigma provides technical indicators and fundamental data for any given stock or digital asset - Stock Screening
The Terminal provides the latest news and company specific news
Sigma Terminal allows users to analyze Twitter, Reddit and common news sites sentiment to identify stocks and give broad market information
The terminal uses AI to identify a users optimal portfolio combination
Users can recreate their portfolio, have watchlists and track portfolio performance

# Data Structure:
Python Script is running and executing on a hosted server
In Python, the data is constantly queried from API’s, RSS feeds and other plugs
Then, the data is stored as a dictionary in MongoDB and stored for 3 days
Whenever a user accesses data in the Web Application, the data is provided through querying the Mongo DB
