import urllib.request
import csv
from bs4 import BeautifulSoup

import numpy as np
import multiprocessing as multi
import sys
import threading

def chunks(n, page_list):
    return np.array_split(page_list,n)

csvWriteLock = threading.Lock()

from queue import Queue

desiredTableHeads = [ "Name", "What", "Region", "Country", "Lat", "Long", "Elev ft.", "Pop est" ]

def find_all_the_links(page_ranges):
	with open('output.csv', 'a') as csvfile:
		fieldnames = ['City', 'State', 'Latitude', 'Longitude', 'Elevation', 'EstmdPopulation']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		my_queue = Queue(maxsize = 0)
		for pages in page_ranges:
			my_queue.put(pages)
		data = []
		while (my_queue.empty() == False):
			url = my_queue.get()
			try:
				page = urllib.request.urlopen(url)
			except:
				print("Some error occured while opening URL")
			soup = BeautifulSoup(page, "html.parser")
			all_tables = soup.find_all('table')
			if(len(all_tables) != 0):	
				for table in all_tables:
					rows = table.find_all("tr")
					th = []
					for cells in rows[0].find_all('th'):
						th.append(str(cells.get_text()))
					if (th == desiredTableHeads):
						for i in range(1, len(rows)):
							data_list = rows[i].find_all('td')
							data = {}
							data.update({'City': data_list[0].text,
                            	    'State': data_list[2].text,
                                	'Latitude': data_list[4].text,
                 	               'Longitude': data_list[5].text,
                    	            'Elevation': data_list[6].text,
                        	        'EstmdPopulation': data_list[7].text
                            	    })
							#print (data)
							with csvWriteLock:
								writer.writerow(data)
			links = soup.find_all('a')		
			for link in links:
				newFoundUrl = prefix + link.get('href')
				if(newFoundUrl == prefix+"../"):
					continue
				if(".html" not in newFoundUrl):
					my_queue.put(newFoundUrl)
 

cpus = multi.cpu_count()
workers = []
site = "http://www.fallingrain.com/world/IN/"
prefix = "http://www.fallingrain.com"

page_list = [site + '00', site + '01', site + '02', site + '03', site + '05', site + '06', site + '07', site + '09', site + '10', site + '11', site + '12', site + '13', site + '14', site + '16', site + '17', site + '18', site + '19', site + '20', site + '21', site + '22', site + '23', site + '24', site + '25', site + '26', site + '28', site + '29', site + '30', site + '31', site + '32', site + '33', site + '34', site + '35', site + '36', site + '37', site + '38', site + '39',]

page_bins = chunks(cpus, page_list)


for cpu in range(cpus):
    #sys.stdout.write("CPU " + str(cpu) + "\n")
    worker = multi.Process(name=str(cpu), 
                           target=find_all_the_links, 
                           args=(page_bins[cpu],))
    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join()
    