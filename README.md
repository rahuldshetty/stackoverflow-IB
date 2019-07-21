# stackoverflow-IBM 
Phoenix Search is a Stack Overflow Exclusive Search Engine which uses a indexed database to extract the top relevant questions based on your query. It analyses the top asnwers from the extracted questions from Stack Overflow, and then computes with a probability that the given answer is relevant or not.

## Live Demo
The Project is deployed in Heroku. Follow this link to visit the website: [Heroku Link](https://phoenix-search-app.herokuapp.com/)

## Installation

1) Clone the repository on your system. `git clone https://github.com/rahuldshetty/stackoverflow-IBM.git`

2) Install Python 3 and all the modules specified in the 'requirements.txt' file. Use pip to install the commands as `pip install flask requests bs4 whoosh stackapi`

3) Change the host and port from 'server.py' . Defaults are set to work with heroku.

3) Run 'server.py' in python as `python server.py` and visit the address that was specified on your browser.
