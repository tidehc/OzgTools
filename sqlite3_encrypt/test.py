# coding=utf-8

import sys
import os
import hashlib
import sqlite3
import cfg

reload(sys) 
sys.setdefaultencoding("utf8")

if __name__ == "__main__":
	
	db = sqlite3.connect(cfg.db_path)
	db.row_factory = sqlite3.Row

	#查询所有表
	cur_table = db.cursor()
	sql = "select * from sqlite_master";
	cur_table.execute(sql)
	tables = cur_table.fetchall()

	for table in tables:
		#循环所有表，sqlite_sequence除外
		if not table["name"] == "sqlite_sequence":

			#查询对应表的所有数据
			cur_row = db.cursor()
			sql = "select * from " + table["name"]
			cur_row.execute(sql)
			rows = cur_row.fetchall()
			for row in rows:

				#循环对应表的所有数据

				row_str = table["name"]
				for row_field in row:
					#将所有字段的内容拼起来，cfg.encrypt_field_name指定的字段除外
					if not row_field == row[cfg.encrypt_field_name]:
						row_str += str(row_field)
				#md5处理
				row_str = cfg.encrypt_template.format(row_str = row_str)
				row_str = hashlib.md5(row_str)
				encrypt_key = row_str.hexdigest()

				if encrypt_key == row[cfg.encrypt_field_name]:
					print "Table " + table["name"] + " id is " + str(row["id"]) + " valid ok"
				else:
					print "Table " + table["name"] + " id is " + str(row["id"]) + " valid error"


	db.close()
	print "Finish!"
