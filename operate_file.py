""" 画像ファイルへの処理をするclassを記述 """

import os
import pathlib
import shutil

import change_time_format


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
		print('get_pictures file_names: ', file_names)

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

			print('picture_path file_names[0]: ', file_names[0])
			file_name = file_names[0]

			return file_names[0]

		# pic_flagがFalseだったら、temp_pathからファイル名を取得する
		path_obj = pathlib.Path(self.temp_path)
		file_names = [p.name for p in path_obj.iterdir() if p.is_file()]
		
		print('temp_path file_names[0]: ', file_names[0])
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
		print('origin_path: ', origin_path)

		# 画像の作成日時を取得する
		path_obj = pathlib.Path(origin_path)
		# file_time = path_obj.stat().st_ctime
		file_time = path_obj.stat().st_birthtime
		print('file_time: ', file_time)
		print('type: ', type(file_time))

		# 日時のフォーマットを変更
		time_obj = change_time_format.Change_time_format(file_time)
		formatted_time = time_obj.change_to_str()
		print('formatted_time: ', formatted_time)
		print('type: ', type(formatted_time))

		# 新画像名のpath
		renamed_path = self.picture_path + formatted_time + '.jpg'
		print('renamed_path: ', renamed_path)

		# renameする処理
		os.rename(origin_path, renamed_path)

		# renameされた画像名を取得する
		path_obj = pathlib.Path(self.picture_path)
		renamed_names = [p.name for p in path_obj.iterdir() if p.is_file()]
		renamed_name = renamed_names[0]
		print('rename_picture name: ', renamed_name)
		print('rename_picture name type: ', type(renamed_name))

		return renamed_name


	def move_picture(self, pic_name):
		"""画像ファイルを移動するfunction
		Args:
			pic_name (str): renameされた画像ファイルの名前
		"""
		origin_path = self.picture_path + pic_name

		moved_path = shutil.move(origin_path, self.temp_path)

		print('moved_path: ', moved_path)
		print('moved_path type: ', type(moved_path))


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
		





		






