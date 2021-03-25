#!/usr/local/bin/bash

echo "Hello World"

PICTURE_PATHS=("./cam001" "./cam002" "./cam003")
TEMP_PATHS=("./temp/temp001/" "./temp/temp002/" "./temp/temp003/")
ORIGINAL_PATHS=("./original/original001/" "./original/original002/" "./original/original003/")
RENAMED_PATHS=("./renamed/renamed001/" "./renamed/renamed002/" "./renamed/renamed003/")


# 画像ファイルのpath(文字列)から画像ファイルの連番だけを切り出す処理
function cut_str(){
	# fileのpathを切り取り画像ファイルの連番だけ取得する
	FIRST_CUT="$(echo $1 | cut -c 16-)"
	SECOND_CUT="$(echo $FIRST_CUT | rev | cut -c 5- | rev)"
}


for ((i=0; i<3; i++))
do
	# fileの存在確認　(-n: fileが存在すればtrueを返す)
	if [ -n "$(ls ${PICTURE_PATHS[$i]})" ]; then
		#echo ${PICTURE_PATHS[$i]}
		# file数を取得し、変数NUMに格納
		NUM="$(ls -1U ${PICTURE_PATHS[$i]} | wc -l)"
		#echo $NUM

		# file数が 2つ以上あるか確認し、条件分岐
		if [ $NUM -gt 1 ]; then
			# 画像ファイルの連番の最大値を格納する変数
			MAX=0
			# 画像ファイルの連番の最大値のindexを格納する変数
			MAX_IDX=0
			#counter変数
			COUNTER=0
			#echo $MAX

			declare -a FILES=()
			#echo $FILES
			# ディレクトリ内から ,txtファイルを1つずつ抜き出す
			for j in ${PICTURE_PATHS[$i]}/*.txt
			do
				FILES+=($j)
				# 画像ファイルの連番を取得
				cut_str $j ${PICTURE_PATHS[$i]}
				#echo $SECOND_CUT
				# 連番の最大値を取得
				if [ $SECOND_CUT -gt $MAX ]; then
					MAX=$SECOND_CUT
					#echo $MAX
					MAX_IDX=$COUNTER
					#echo $MAX_IDX
					COUNTER=$(($COUNTER + 1))
					#echo $COUNTER
				fi
			done
			echo ${#FILES[*]}
			# ディレクトリ内の最新の画像ファイルを変数に格納
			LATEST_FILE=${FILES[$MAX_IDX]}
			#echo $LATEST_FILE
			# ディレクトリ内の最新の画像ファイルを削除
			unset FILES[$MAX_IDX]
			#echo ${#FILES[@]}

			# 最新の画像ファイル以外に対する処理
			for ((k=0; k<${#FILES[@]}; k++))
			do
				# original画像名格納フォルダにcopy
				cp ${FILES[$k]} ${ORIGINAL_PATHS[$i]}
				# 画像ファイルの日時を取得する
				file_date=`date -r ${FILES[$k]} +"%Y-%m-%d_%H:%M"`
				echo $file_date
				# rename画像名格納フォルダへのpathを作成
				MOVED_FILE_DATE="${RENAMED_PATHS[$i]}${file_date}.txt"
				echo $MOVED_FILE_DATE
				# 画像ファイルをrename画像名格納フォルダにmove
				mv ${FILES[$k]} $MOVED_FILE_DATE
			done
		fi

		# tempフォルダの画像ファイルの存在確認
		if [ -n "$(ls ${TEMP_PATHS[$i]})" ]; then
			# 画像ファイルのpathを取得
			TEMP_FILE=${TEMP_PATHS[$i]}*.txt
			echo $TEMP_FILE
			# 画像ファイルをrename画像名格納フォルダにmove
			mv $TEMP_FILE ${RENAMED_PATHS[$i]}
		fi

		#

		# 画像ファイルのpathを取得
		LATEST="${PICTURE_PATHS[$i]}/*.txt"
		echo $LATEST
		# original画像名格納フォルダにcopy
		cp $LATEST ${ORIGINAL_PATHS[$i]}
		# 画像ファイルの日時を取得する
		DATE=`date -r $LATEST +"%Y-%m-%d_%H:%M"`
		#echo $DATE
		# tempフォルダへのpathを作成
		MOVED_DATE="${TEMP_PATHS[$i]}${DATE}.txt"
		#echo $MOVED_DATE
		# 画像ファイルをtempフォルダにmove
		mv $LATEST $MOVED_DATE

	else
		echo "Nothing"
	fi
done



