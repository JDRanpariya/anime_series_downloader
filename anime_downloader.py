import requests
from bs4 import BeautifulSoup

download_links, download_website_link, file_names, ep_urls = [], [], [], []

website = 'https://www9.gogoanime.io/'
anime_name = input('Enter the name of the anime(as in website url): ')
number_of_episodes = int(input('Enter the number of episodes in anime: '))


print('Generating meta data', end=' ')
for i in range(1, number_of_episodes+1):
	single_ep_url = website + anime_name + '-episode-' + str(i)
	ep_urls.append(single_ep_url)
	file_names.append(anime_name+'-ep-'+str(i)+'.mp4')
	print('.', end='')


print("\ngetting the download website links, This may take a while, Please wait...\n", end=' ')

for i in range(number_of_episodes):
	page = requests.get(ep_urls[i])
	soup = BeautifulSoup(page.content, 'html.parser')
	x = soup.find_all('a', target='_blank')
	download_website_link.append(x[-1]['href'])
	


for link in download_website_link:
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	x = soup.find_all('a', download="")
	
	check = 0
	
	for i in x[::-1]:
		if i.text == 'Download\n            (360P - mp4)':
			download_links.append(i['href'])
			check = 1
			break
		elif i.text == 'Download\n            (480P - mp4)':
			download_links.append(i['href'])
			check = 1
			break
		elif i.text == 'Download\n            (720P - mp4)':
			download_links.append(i['href'])
			check = 1
			break
		elif i.text == 'Download\n            (1080P - mp4)':
			download_links.append(i['href'])
			check = 1
			break
		elif i.text == 'Download\n            (orginalP - mp4)':
			download_links.append(i['href'])
			check = 1
			break

	if check == 0:
		print("\n\nAn episode is missing download link")



for i in range(number_of_episodes):

	r = requests.get(download_links[i], stream = True) 

	print('starting ' + file_names[0] + ' download............')

	with open(file_names[i], 'wb') as f: 
		for chunk in r.iter_content(chunk_size = 1024*1024): 
			if chunk:
				f.write(chunk)

	print('Completed downloading', file_names[i], '\n')	

