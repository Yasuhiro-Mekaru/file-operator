""" 画像ファイルへの処理をするclassを記述 """

import os
import pathlib
import shutil

import change_time_format
import execute_func

# print('os cpu_count: ', os.cpu_count())

class Operate_file(object):
	""" 画像ファイルへの操作を定義したclass """
	def __init__(self, picture_path, temp_path, original_picture_path, renamed_picture_path):
		"""コンストラクタ
		Args:
			picture_path (str): 新規画像ファイルの格納フォルダのpath
			temp_path (str): リネームされた画像ファイルの一時的な格納フォルダのpath
			original_picture_path (str): オリジナルの名前の画像ファイルの格納フォルダのpath
			renamed_picture_path (str): リネームされた画像ファイルの格納フォルダのpath
		"""
		self.picture_path = picture_path
		self.temp_path = temp_path
		self.original_picture_path = original_picture_path
		self.renamed_picture_path = renamed_picture_path


	def get_pictures(self, path):
		"""画像ファイルの存在確認をするfunction
		Args:
			path (str): Path of the folder which you want to confirm existence of picture file.
		Return:
			list: return the picture files list
		"""
		path_obj = pathlib.Path(path)
		file_names = [p.name for p in path_obj.iterdir() if p.is_file()]

		#picture_pathに2つ以上画像ファイルが格納されている際の処理
		if len(file_names) > 1:
			# 最新の画像ファイルindexを取得する
			max_idx = execute_func.sort_pictures(pictures=file_names)

			# 最新の画像ファイルとindex.htmlをfile_namesListから取り出す
			latest_pic = file_names.pop(max_idx)
			new_file_list = [latest_pic]

			for name in file_names:
				# index.htmlファイルが混じっていたら削除する
				if name == 'index.html':
					os.remove(self.picture_path + 'index.html')
				else:
					# originalフォルダにcopyする
					self.copy_picture(pic_name=name, is_origin=True)
					# 画像の作成日時を取得する
					origin_path = self.picture_path + name
					path_obj = pathlib.Path(origin_path)
					file_time = path_obj.stat().st_birthtime
					# 日時のフォーマットを変更
					time_obj = change_time_format.Change_time_format(file_time)
					formatted_time = time_obj.change_to_str()
					#　新画像名を定義する
					renamed = formatted_time + '.jpg'
					# 新画像名のpathを定義する
					renamed_path = self.picture_path + renamed
					# renameする処理
					os.rename(origin_path, renamed_path)
					# renamedフォルダへcopy
					self.copy_picture(pic_name=renamed, is_origin=False)
					# removeする処理
					os.remove(renamed_path)
			# 最新の画像ファイルだけをreturnする
			return new_file_list

		return file_names


	def get_picture_name(self, pic_flag):
		"""画像ファイル名を取得するfunction
		Args:
			pic_flag (bool): 新規の画像ファイルがあるか判定するフラグ
		Return:
			str: return the picture name
		"""
		# pic_flagがTrueだったら、picture_pathからファイル名を取得する
		if pic_flag:
			path_obj = pathlib.Path(self.picture_path)
			file_names = [p.name for p in path_obj.iterdir() if p.is_file()]
			file_name = file_names[0]

			return file_name

		# pic_flagがFalseだったら、temp_pathからファイル名を取得する
		path_obj = pathlib.Path(self.temp_path)
		file_names = [p.name for p in path_obj.iterdir() if p.is_file()]

		#temp_dirに画像ファイルが無い場合はそのまま空のListを返す
		if not file_names:
			return file_names

		file_name = file_names[0]
		return file_name


	def renamed_picture_name(self, pic_name):
		"""画像ファイルをrenameするfunction
		Args:
			pic_name (str): 新規画像ファイルの名前
		Return:
			str: return the picture name
		"""
		# 元画像名のpath
		origin_path = self.picture_path + pic_name

		# 画像の作成日時を取得する
		path_obj = pathlib.Path(origin_path)
		# file_time = path_obj.stat().st_ctime
		file_time = path_obj.stat().st_birthtime

		# 日時のフォーマットを変更
		time_obj = change_time_format.Change_time_format(file_time)
		formatted_time = time_obj.change_to_str()

		# 新画像名のpath
		renamed_path = self.picture_path + formatted_time + '.jpg'

		# renameする処理
		os.rename(origin_path, renamed_path)

		# renameされた画像名を取得する
		path_obj = pathlib.Path(self.picture_path)
		renamed_names = [p.name for p in path_obj.iterdir() if p.is_file()]
		renamed_name = renamed_names[0]

		return renamed_name


	def move_picture(self, pic_name):
		"""画像ファイルを移動するfunction
		Args:
			pic_name (str): renameされた画像ファイルの名前
		"""
		origin_path = self.picture_path + pic_name

		moved_path = shutil.move(origin_path, self.temp_path)


	def copy_picture(self, pic_name, is_origin):
		"""画像ファイルをcopyするfunction
		Args:
			pic_name (str): copyする画像ファイルの名前
			is_origin (bool): 画像ファイル名がオリジナルか判定するフラグ
		"""
		# copy元画像ファイルのpath
		path = self.picture_path + pic_name

		if is_origin:
			# 元画像名用のディレクトリへcopy
			shutil.copy(path, self.original_picture_path)
		else:
			# 新画像名用のディレクトリへcopy
			shutil.copy(path, self.renamed_picture_path)


	def remove_picture(self, pic_name):
		"""画像ファイルをremoveするfunction
		Args:
			pic_name (str): removeする画像ファイルの名前
		"""
		# removeする画像ファイルのpath
		path = self.temp_path + pic_name
		# 画像ファイルのremove
		os.remove(path)
		





		






