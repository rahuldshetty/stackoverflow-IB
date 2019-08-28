# stackoverflow-IBM 
Phoenix Search is a Stack Overflow Exclusive Search Engine which uses a indexed database to extract the top relevant questions based on your query. It analyses the top asnwers from the extracted questions from Stack Overflow, and then computes with a probability that the given answer is relevant or not.

## Video Link
![Youtube Link](https://youtu.be/cRmtmLGRU1c)

## Installation

1) Clone the repository on your system. `git clone https://github.com/rahuldshetty/stackoverflow-IBM.git`

2) Install Python 3 and all the modules specified in the 'requirements.txt' file. Use pip to install the commands as `pip install requirements.txt`

3) Change the host and port from 'server.py'. Default is set to `127.0.0.1:5000`

4) Run 'server.py' in python as `python server.py` and visit the address that was specified on your server file.

`Note: You can increase the value of COUNT and page_begin from 'collect_dataset.py to scrap in more urls from Stack Overflow. Better Search results are obtained by increaseing these parameters. Run this python script to add in more samples.'`