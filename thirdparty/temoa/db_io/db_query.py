import sqlite3
import os
import sys
import getopt


def send_query(inp_f, query_string):
	db_result = []
	try:
		con = sqlite3.connect(inp_f)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

		print inp_f
		cur.execute(query_string)
		import pdb;pdb.set_trace()
		for row in cur:
			db_result.append(row)
		
		cur.close()
		con.close()
		return db_result
	except sqlite3.Error, e:
		print "Error in Query %s:" % e.args[0]
		sys.exit(1)
		
		
if __name__ == "__main__":
	print send_query("temoa_utopia.sqlite","SELEC DISTINCT t_periods FROM Output_VFlow_Out WHERE scenario is 'test_run'")