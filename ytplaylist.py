import json
from sys import argv
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

with open('data.csv', 'w') as f:
	f.write('title, views\n')

with open('ytplaylist.json', 'r') as f:
	data = json.load(f)

profile = webdriver.FirefoxProfile()
profile.set_preference('media.volume_scale', '0.0')

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=data['geckodriver'])

driver.get(argv[1])

# scrape the title, views, date, length of playlist
count = 1
playlist_len = int(argv[2])

while True:
	sleep(2)
	
	title = driver.find_element_by_class_name('title').text
	print(title)
	
	views = driver.find_element_by_class_name('view-count').text
	print(views)

	views = views.replace(',', '')
	views = views.replace(' views', '')

	next_vid = driver.find_element_by_class_name('ytp-next-button').click()

	with open('data.csv', 'a') as csv:
		csv.write(f'{title}, {views}\n')

	if count == playlist_len:
		break
	else:
		count += 1

driver.close()