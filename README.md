# ArcgisPapaTransfer
arcgis shp 文件 坐标系 文件转换
参数 --type 
支持
wgs2gcj bd2gcj

带转换文件路径 --path "C:\目标文件夹"

自动查询path目录下的shp文件,将文件坐标系转化为火星GCJ-02坐标系文件,并保存转换完成后的shp文件于目录下OutPut文件夹中

依赖coord-convert  https://github.com/sshuair/coord-convert  ,在coord-convert基础上进行的开发

成品目录 在dist下 
运行命令 convert --type "wgs2gcj" --path "目标文件夹路径(结尾不需要\)"
