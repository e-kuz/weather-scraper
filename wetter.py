from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

print("This program shows when there are good days")
print("for a run outside in the next week.")
print("A day is considered good if:")
print("-it is warmer than 8°C")
print("-it isn't raining on that day")
print("-and it hasn't rained in the last 24 hours (so the roads aren't wet)")

print("The data is scraped from the \"wetter.de\" website using BeautifulSoup\n")

# get the page with weather forecasts for the next 7 days in Bochum
wetterurl = 'https://www.wetter.de/deutschland/wetter-bochum-18220925/wetter-uebersicht.html'
uClient = urlopen(wetterurl)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")


# going to store the results in a list of 28 lists, with Date as 1st element,
# time as 2nd, temp in °C (int) as 3rd element, rain(Yes/No) as 4th element
# (there are 28 lists since there are 7 days with 4 times each)
temps = [[] for i in range(28)]



# extracts the whole forecasts for the next 7 days
forecasts = page_soup.findAll("div",{"class": "forecast-list list-standard"})

for i in range(len(forecasts)):
    forecast = forecasts[i]
    
    # get day of week and date
    day = forecast.find("div",{"class": "text-day"})
    date = forecast.find("div",{"class": "text-date"})

    # get the time of the day
    # (there are forecasts for 01:00, 07:00, 13:00 and 19:00 every day)
    times = forecast.findAll("div",{"class": "forecast-column-date"})

    # get the temperatures
    degrees = forecast.findAll("div",{"class": "forecast-text-temperature"})


    # fill in date+time and the temperatures 
    for j in range(len(times)):
        fulldate = day.text + " " + date.text
        temps[i*4+j].append(fulldate)
        temps[i*4+j].append(times[j].text)
        # text is used without the last char to strip the ° symbol
        temps[i*4+j].append(int(degrees[j].text[:-1]))


    # get the rain forecasts, different structure from temperatures
    # risk of rain and amount of rain are displayed in separate "span" tags,
    # if the risk is 0, the amount "span" does not exist
    rains = forecast.findAll("div",{"class": "forecast-column-rain"})
    for r in range(len(rains)):
        riskandamount = rains[r].findAll("span",{"class": "wt-font-semibold"})
        # if risk is 0, len of nums is 1
        if len(riskandamount)==1:
            temps[i*4+r].append("No")
        else:
            # if it rains less than one litre per square metre, count that as no
            if (riskandamount[1].text.startswith("<")
                    or riskandamount[1].text.startswith("0,")):
                temps[i*4+r].append("No")
            else:
                 temps[i*4+r].append("Yes")
                


# collected all the data, now find "good" days
counter = 0
for i in range(4,len(temps)):
    if temps[i][1]!="01:00" and temps[i][2]>=8:
        if all(t[3] == "No" for t in temps[i-4:i+1]):
            print(temps[i][0], temps[i][1], " is a good day for a run!")
            counter +=1
if counter==0:
    print("There are no good days for a run ")
            
        
        


