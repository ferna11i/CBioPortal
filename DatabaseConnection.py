import requests as req

url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/init.php";

response = req.get(url)

data = response.json()
print(data)

for value in data:
    print("{} {}".format(value['ID'], value['Name']))
