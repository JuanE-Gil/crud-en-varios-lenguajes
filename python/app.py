import db.database as sqldb

data_base = sqldb.DataBase(**sqldb.access_db)

#data_base.show_db()
data_base.create_db("test")
#data_base.eliminate_db("test")
