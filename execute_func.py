""" 新規画像がある時の処理を実行するfunctionを記述 """

import operate_file


# 新規の画像ファイルがあるか判定するフラグ(初期値: False)
is_pic = False
# 画像ファイル名がオリジナルか判定するフラグ(初期値: False)
is_origin = False


def exec_origin_picture(pic_instance, temp_path):
	"""新規画像がある時の処理をまとめたfunction
	Args:
		pic_instance (object): Operate_fileインスタンス
		temp_path (str): renameされた画像を一時的に格納するためのフォルダのpath
	"""
	is_pic = True

	# 画像ファイル名を取得する
	origin_pic_name = pic_instance.get_picture_name(pic_flag=is_pic)
	print('origin_pic_name: ', origin_pic_name)
	print('origin_pic_name type: ', type(origin_pic_name))
	is_pic = False

	# 画像ファイルをoriginal_pictureにcopyする
	is_origin = True
	pic_instance.copy_picture(pic_name=origin_pic_name, is_origin=is_origin)
	is_origin = False

	# 画像ファイルをrenameする
	renamed_pic_name = pic_instance.renamed_picture_name(pic_name=origin_pic_name)
	print('renamed_pic_name: ', renamed_pic_name)
	print('renamed_pic_name type: ', type(renamed_pic_name))

	# 画像ファイルをrenamed_pictureにcopyする
	if is_origin:
		is_origin = False
	pic_instance.copy_picture(pic_name=renamed_pic_name, is_origin=is_origin)

	# temp_dirに画像ファイルがあるか確認
	temp_list = pic_instance.get_pictures(path=temp_path)
	print('temp_list: ', temp_list)

	# tempフォルダに画像ファイルがあればremoveする
	if temp_list:
		if is_pic:
			is_pic = False
		old_pic_name = pic_instance.get_picture_name(pic_flag=is_pic)
		pic_instance.remove_picture(pic_name=old_pic_name)

	# 画像ファイルをtempフォルダにmoveする
	pic_instance.move_picture(pic_name=renamed_pic_name)