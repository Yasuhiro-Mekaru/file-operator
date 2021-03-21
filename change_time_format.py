""" 時間を扱う処理について記述 """

import datetime


class Change_time_format(object):
	""" 画像ファイルのtime formatを変更するclass """
	def __init__(self, file_time):
		"""コンストラクタ
		Args:
			file_time (float): 画像ファイルの更新日時(エポック秒)
		"""
		self.file_time = file_time
		self.dt = self.change_to_datetime()


	def change_to_datetime(self):
		"""エポック秒をdatetime型に変換するfunction
		Return:
			datetime: 画像ファイルの更新日時(datetime型)
		"""
		dt = datetime.datetime.fromtimestamp(self.file_time)
		# print('dt: ', dt)
		# print('type: ', type(dt))

		return dt


	def change_to_str(self):
		"""datetime型をformatに基づいたstr型に変換するfunction
		Return:
			str: 画像ファイルの更新日時(str型)
		"""
		# formatを設定
		time_format = '%Y-%m-%d_%H:%M'

		str_time_format = self.dt.strftime(time_format)
		# print('str_time_format: ', str_time_format)
		# print('type: ', type(str_time_format))

		return str_time_format
