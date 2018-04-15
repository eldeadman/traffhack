from bs4 import BeautifulSoup
import re
import datetime
import os

# CSV HEADERS: post_id, location, time_stamp, poster_age, gender, phone
def restart_file():
    dat = open('/home/maggie/Documents/human_trafficking/backpage_data.csv', 'w')
    row = 'post_id, city, county, state, time_stamp, age, gender, phone'
    dat.write(row)
    dat.close()

#restart_file()

dat = open('/home/maggie/Documents/human_trafficking/backpage_data.csv', 'a')
count = 79 # change here
start = count + 2

path = '/home/maggie/Documents/human_trafficking/backpage/'
os.chdir('/home/maggie/Documents/human_trafficking/backpage/')
for f in os.listdir(path)[start:]:
    with open (f) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    
    # TIME
    time_stamp = soup.find(attrs={'class':'adInfo'})
    if time_stamp == None:
        time_stamp = ' '
    elif len(time_stamp) == 0:
        time_stamp = ' '
    else:
        time_stamp = re.findall('[MTWFS].*[APM]', time_stamp.string.encode('utf8'))[0]
        time_stamp = str(datetime.datetime.strptime(time_stamp, "%A, %B %d, %Y %I:%M %p"))
    
    
    # LOCATION
    loc = soup.find_all('div', attrs={'style':'padding-left:2em;'})
    if loc == None:
        loc = ' '
    elif len(loc) == 0:
        loc = ' '
    else:
        loc = loc[0].string.encode('utf8')
        loc = re.findall('([A-Za-z]+,.*)\r', loc)
        if len(loc) == 0:
            loc = soup.find_all('div', attrs={'style':'padding-left:2em;'})
            loc = re.findall('Location:\r\n\s+([A-Za-z]*)', loc[0].string.encode('utf8'))
    
        if len(re.findall(',', loc[0]))==0:
            loc = loc[0] + ', , '
        elif len(re.findall(',', loc[0]))==1:
            loc = loc[0].split(',')[0] + ', ,' + loc[0].split(',')[1] 
        else:
            loc = loc[0]
            
    
    # AGE
    age = soup.find('p', class_='metaInfoDisplay')
    if age == None:
        age = ' '
    elif len(age) == 0:
        age = ' '
    else:
        age = re.findall('[0-9]+', str(age))
    
    
    # POST ID
    post_id = soup.find_all('div', attrs={'style':'padding-left:2em;'})
    if post_id == None:
        post_id = ' '
    elif len(post_id) == 0:
        post_id = ' '
    else:
        post_id = str(soup.find_all('div', attrs={'style':'padding-left:2em;'})[1])
        post_id = re.findall('Post ID: ([0-9]*)', post_id)
    
    
    # PHONE NUMBER
    phone = soup.find('div', class_='postingBody')
    if phone == None:
        phone = ' '
    elif len(phone) == 0:
        phone = soup.li.img['title']
        if phone == None:
            phone = ' '
    else:
        phone = re.findall(':.(.[0-9)-].*)<', str(phone))
    
    
    # GENDER
    gender_convert = {'/WomenSeekMen': 'Female', '/WomenSeekWomen':'Female', 
                      '/MenSeekMen':'Male', '/MenSeekWomen':'Male'}
    stop = False
    gender = soup.find_all('li')
    if gender == None:
        gender = ' '
    elif len(gender) == 0:
        gender = ' '
    else:
        while stop == False:
            for row in gender:
                if len(re.findall('Men', str(row))) != 0:
                    gender = row.a['href']
                    stop = True
        gender = gender_convert[re.findall('com(.+/*Seek.+?)/', gender)[0]]
    
    row = '\n' + post_id[0] + ',' + loc + ',' \
      + time_stamp + ',' + age[0] + ',' + gender[0] + ',' + phone[0]
        
    dat.write(row)
    count += 1
    print('Completed: %s, %s done' % (f, count))

print('done')
dat.close()