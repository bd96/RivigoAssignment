# Web Scrapper

It is an online tool which is used to collect relevant information from the [website](http://www.fallingrain.com/world/IN/). 

## How to execute

1. **Pre-requisites**
 
* BeautifulSoup
```bash
sudo apt-get install python3-bs4
```

* Numpy
```bash
sudo apt-get install python3-numpy
```

2. Execute the RivigoAss.py
```bash
python3 RivigoAss.py
```
## Implementation
1. Web Scrapping is used to extract data from websites so they can be used in analysis. In order to exctract all the information about citites in the link we first inspected the HTML page to find out patterns which help us identify important information about the city. The page had multiple links divided on the basis of state then on their names. 
2. I found out that our information can be extracted from the page having table tag with the desired table heads. I traversed all the pages one by one and looked for the particular table tag. I used queue for storing all the links.
3. Since the number of links were very large, the execution could have taken a long time. So to handle it, i used the concept of mulithreading it it which redued the time of execution to a very large extent.

_The csv file was not completed at the time of submission, please bear with me._
