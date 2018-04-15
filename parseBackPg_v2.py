from bs4 import BeautifulSoup
import re
import datetime
import os

def restart_file():
    dat = open('/home/maggie/Documents/human_trafficking/backpage/backpage_data.csv', 'w')
    row = 'post_id, time_stamp, age, phone, loc1, loc2, loc3, loc4'
    dat.write(row)
    dat.close()

#restart_file()


dat = open('/home/maggie/Documents/human_trafficking/backpage/backpage_data.csv', 'a')

count = 721
start = count + 2

path = '/home/maggie/Documents/human_trafficking/backpage/backpage.com/'
os.chdir(path)
for f in os.listdir(path)[start: ]:

    with open(f) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    
    
    time_stamp = soup.find(attrs={'class':'adInfo'}).string.encode('utf8')
    time_stamp = str(datetime.datetime.strptime(re.findall('[MTWFS].*[APM]', time_stamp)[0], "%A, %B %d, %Y %I:%M %p"))
    
    
    loc = soup.find('div', attrs={'style':'padding-left:2em;'}).string.encode('utf8')
    loc = re.findall('([A-Za-z]+,.*)\r', loc)
    
    if len(loc) == 0:
        loc = soup.find('div', attrs={'style':'padding-left:2em;'}).string.encode('utf8')
        loc = re.findall('Location:\r\n\s+([A-Za-z]*)', loc)
                    
    
    age = soup.find('p', class_='metaInfoDisplay')
    age = re.findall('[0-9]+', str(age))
    
    post_id = soup.find_all('div', attrs={'style':'padding-left:2em;'})[1]
    post_id = str(soup.find_all('div', attrs={'style':'padding-left:2em;'}))
    post_id = re.findall('Post ID: ([0-9]*)', post_id)
    
    phone = soup.find('div', class_='postingBody')
    phone = re.findall(':.(.[0-9)-].*)<', str(phone))
    

    row = '\n' + post_id[0] + ',' \
          + time_stamp + ',' + age[0] + ',' + phone[0] + ',' + loc[0]
            
    dat.write(row)
    count += 1
    print('Files done: %s, Completed %s' % (count, f))
dat.close()        
