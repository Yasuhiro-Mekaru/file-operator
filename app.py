#!/home/seedplus-cam/.pyenv/versions/3.8.1_flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

import execute_func
import operate_file


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
	# 各カメラ毎の画像が送られてくるフォルダのpath
	picture_path_1 = '/home/seedplus-cam/www/cam001/'
	picture_path_2 = '/home/seedplus-cam/www/cam002/'
	picture_path_3 = '/home/seedplus-cam/www/cam003/'

	# renameされた画像を一時的に格納するためのフォルダのpath
	temp_path_1 = '/home/seedplus-cam/www/temp/temp001/'
	temp_path_2 = '/home/seedplus-cam/www/temp/temp002/'
	temp_path_3 = '/home/seedplus-cam/www/temp/temp003/'
	temp_path_lists = [temp_path_1, temp_path_2, temp_path_3]

	# 画像をオリジナルの名前で保存するためのフォルダのpath
	original_picture_path_1 = '/home/seedplus-cam/www/original/original001/'
	original_picture_path_2 = '/home/seedplus-cam/www/original/original002/'
	original_picture_path_3 = '/home/seedplus-cam/www/original/original003/'

	# renameされた画像を保存するためのフォルダのpath
	renamed_picture_path_1 = '/home/seedplus-cam/www/renamed/renamed001/'
	renamed_picture_path_2 = '/home/seedplus-cam/www/renamed/renamed002/'
	renamed_picture_path_3 = '/home/seedplus-cam/www/renamed/renamed003/'

	# 新規の画像ファイルがあるか判定するフラグ(初期値: False)
	is_pic = False

	operate_lists = []
	# 画像ファイルを処理するためのOperate_fileインスタンスを生成
	# 1つ目のカメラ画像
	operate_1 = operate_file.Operate_file(picture_path_1, temp_path_1, original_picture_path_1, renamed_picture_path_1)
	operate_lists.append(operate_1)
	# 2つ目のカメラ画像
	operate_2 = operate_file.Operate_file(picture_path_2, temp_path_2, original_picture_path_2, renamed_picture_path_2)
	operate_lists.append(operate_2)
	# 3つ目のカメラ画像
	operate_3 = operate_file.Operate_file(picture_path_3, temp_path_3, original_picture_path_3, renamed_picture_path_3)
	operate_lists.append(operate_3)


	pic_lists = []
	# 新規の画像ファイルが送信されているか確認
	pic_list_1 = operate_1.get_pictures(path=picture_path_1)
	pic_lists.append(pic_list_1)
	print('pic_list_1: ', pic_list_1)
	print('pic_list_1 type: ', type(pic_list_1))

	pic_list_2 = operate_2.get_pictures(path=picture_path_2)
	pic_lists.append(pic_list_2)
	print('pic_list_2: ', pic_list_2)

	pic_list_3 = operate_3.get_pictures(path=picture_path_3)
	pic_lists.append(pic_list_3)
	print('pic_list_3: ', pic_list_3)

	# Jinjaを通してJavascriptへ引き渡すデータを格納するList
	picture_infos = []
	# tempフォルダに格納されている画像への処理
	for pic_list, operate_list, temp_path_list in zip(pic_lists, operate_lists, temp_path_lists):
		# 新規画像がある場合
		if pic_list:
			execute_func.exec_origin_picture(pic_instance=operate_list, temp_path=temp_path_list)

		# 新規画像がない場合 & 新規画像への処理が終わった後
		# temp_dirに格納されている画像ファイル名を取得する
		picture_name = operate_list.get_picture_name(pic_flag=is_pic)
		print('operate_list: ', operate_list)
		print('picture_name: ', picture_name)

		# temp_dirに画像ファイルが無い場合、0を代入する
		if not picture_name:
			picture_name = False

		picture_infos.append(picture_name)


	print('picture_infos: ', picture_infos)
	return render_template('index.html', picture_infos=picture_infos)



if __name__ == '__main__':
	app.run()

