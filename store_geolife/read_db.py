import MySQLdb

def select_points(db, iduser,datestart, dateend):
	sql = "SELECT latitude,longitude,date FROM POINT WHERE iduser = '%d'  AND date > '%s' AND date < '%s'"%\
	(iduser,datestart.strftime("%Y-%m-%d %H:%M:%S"),dateend.strftime("%Y-%m-%d %H:%M:%S"))
	print datestart,dateend
	print sql
	try:
		curs = db.cursor()
		curs.execute(sql)
		res = curs.fetchall()
	except Exception, e:
		print e

	return res

