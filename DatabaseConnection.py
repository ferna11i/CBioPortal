import pymysql as sql

# db = sql.connect(host='myweb2.cs.uwindsor.ca:3306',
#                  user='ferna11i@localhost',    #ferna11i_cb
#                  password='test123',
#                  db='ferna11i_cbioportal')


db = sql.connect(host='mysql2.000webhost.com',
                 user='id6399047_fern_cbioportal',    #ferna11i_cb
                 password='test123',
                 db='id6399047_fern_cb')

cursor = db.cursor()
