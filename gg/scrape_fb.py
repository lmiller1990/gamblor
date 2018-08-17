import urllib.request

URL = 'https://www.bet365.com.au/?rn=26667060391&stf=1#/AC/B151/C20584930/D1/E37268145/F2/'
data = urllib.request.urlopen(URL)
mybytes = data.read()
mystr = mybytes.decode("utf8")
data.close()
print(mystr)

