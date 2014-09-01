# coding=utf-8

#思路是将table_name和所有字段的内容拼接起来，然后经过cfg.encrypt_template再格式化一次，最后再md5一次，写入到对应表的cfg.encrypt_field_name字段。
#验证的时候用上面的办法，然后比较cfg.encrypt_field_name字段，相等则通过验证，不相等则该数据被修改过。
#对于新增数据或更新过的数据，也要写入一下cfg.encrypt_field_name字段。

#这样的实现方式好处是可以不受语言和平台的限制，坏处是逻辑复杂了一些，同时也牺牲了一点性能（但不明显）

import sys
import os
import hashlib
import sqlite3
import cfg

reload(sys) 
sys.setdefaultencoding("utf8")

if __name__ == "__main__":
	
	db_path =  raw_input("请输入数据库的路径:\n")
	
	if db_path == "" or db_path == None:
		db_path = cfg.db_path

	db = sqlite3.connect(db_path)
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
				
				#将md5值写入到cfg.encrypt_field_name指定的字段
				sql = "update " + table["name"] + " set " + cfg.encrypt_field_name + " = '" + encrypt_key + "' where id = " + str(row["id"])
				print "Execute sql: " + sql
				cur_row.execute(sql)
				db.commit()

	db.close()
	print "Finish!"
