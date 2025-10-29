#!/bin/bash

TSN="default_target_name" # target species name 
QSN="default_query_name" # qury species name 
TSG="default_target_genome" # target species genome
QSG="default_qury_genome" # qury species genome
length=10000
identy=80
path2perl="/home/ug2092/script/FilterCoords.pl"

usage(){
echo"$0 --TSN target_name --QSN query_name --TSG target_genome --QSG qury_genome"
echo "optional: --length [filter coords length] --identy [filter coords identy] --path2perl [path to FilterCoords.pl]"
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --TSN)
            TSN="$2"  # 获取参数值
            shift 2       # 跳过当前选项和值
            ;;
        --QSN)
            QSN="$2"
            shift 2
            ;;
        --TSG)
            TSG="$2"
            shift 2
            ;;
	--QSG)
		QSG="$2"
		shift 2
		;;
	--length)
		length="$2"
		shift 2
		;;
	--identy)
		identy="$2"
		shift 2
		;;
	--path2perl)
		path2perl="$2"
		shift 2
		;;
		*)  # 未知选项
            echo "错误：未知参数 $1"
            exit 1
            ;;
    esac
done

mkdir -p ${TSN}-${QSN}

if [ ! -f "${TSN}-${QSN}/nucmerOut.delta" ]; then
	nucmer -p ${TSN}-${QSN}/nucmerOut --threads 32 ${TSG} ${QSG}
fi

delta-filter -i ${identy} -l ${length} ${TSN}-${QSN}/nucmerOut.delta -1 > ${TSN}-${QSN}/nucmerOut.delta.filter

show-coords ${TSN}-${QSN}/nucmerOut.delta.filter > ${TSN}-${QSN}/nucmerOut.delta.filter.coords

perl ${path2perl} ${TSN}-${QSN}/nucmerOut.delta.filter.coords > ${TSN}-${QSN}/nucmerOut.delta.filter.coords.txt
