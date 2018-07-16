import requests as req

# import pymysql as sql
#
# try:
#     # db = sql.connect(host='48588.us-imm-sql6.000webhost.io', #mysql2.000webhost.com
#     #                  user='id6399047_fern_cbioportal',    #ferna11i_cb
#     #                  password='test123',
#     #                  db='id6399047_fern_cb')
#
#     db = sql.connect(host='myweb2.cs.uwindsor.ca',
#                      user='ferna11i_cb',
#                      password='test123',
#                      db='ferna11i_cbioportal')
#
#     cursor = db.cursor()
#
# except Exception as e:
#     print(e)

url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/init.php";

response = req.get(url);

print(response.content);

for value in dict.items(response.content):
    print("{} ".format(value))
