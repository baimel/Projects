# Import necessary libraries
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Get Input to build URL
code = input('Enter Reservoir Code: (CAPS) ')
end = input('Enter End Date: (YYYY-MM-DD) ')
months = input('Enter number of months: ')
url = "https://cdec.water.ca.gov/dynamicapp/QueryMonthly?s="
url1 = url + code
url2 = url1 + "&end=" + end
url3 = url2 + "&span=" + months + "months"

#Read constructed URL
html = urllib.request.urlopen(url3, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

#Extract relevant tags and place in new non-BS4 item
stringlist = list()
soup1 = soup('font')
for tag in soup1:
    tag = str(tag)
    if '000000' in tag:
        stringlist.append(tag)

#Clean data: Slice out what you don't want
cleanlist = list()
for x in stringlist:
    y = x[22:-7]
    if "," in y:
        cleanlist.append(y)

#Clean data: Only take storage numbers; these are even values for index
index = 0
storagelist = list()
for x in cleanlist:
    if index == 0:
        storagelist.append(cleanlist[0])
        index = index + 2
    else:
        if index >= ((float(months) * 2) - 1):
            break
        else:
            storagelist.append(cleanlist[index])
            index = index + 2
            continue

# Format and prep numbers for final calculation
denominator = 0
total = 0
for x in storagelist:
    x = re.sub(',' , '' , x)
    x = float(x)
    print(x)
    total = x + total
    denominator = denominator + 1

#Make final calculation
average = total / denominator
print("Average storage for specified period: ", average, "Acre Feet")
