# -*- coding: utf-8 -*-
import fiona
import math
from tqdm import tqdm
import click
import os
import argparse
from fiona import _shim, schema

from coord_convert.transform import Transform


def recur_map(f, data):
    """递归处理所有坐标

    Arguments:
        f {function} -- [apply function]
        data {collection} -- [fiona collection]
    """

    return [not type(x) is list and f(x) or recur_map(f, x) for x in data]


# convert_type = 'bd2gcj'

# src_path = r'C:\Users\haru\Desktop\万华园区管廊地图（2020-3-1）\宁波底图\宁波底图\DEV_NBFCS_Process_Polygon.shp'

# dst_path = r'C:\Users\haru\Desktop\万华园区管廊地图（2020-3-1）\宁波底图\宁波底图\DEV_NBFCS_Process_Polygon_Out.shp'


def convertor(src_path, dst_path, convert_type):

    with fiona.open(src_path, 'r', encoding='utf-8') as source:
        source_schema = source.schema.copy()
        with fiona.open(dst_path, 'w', encoding='utf-8', **source.meta) as out:
            transform = Transform()
            f = lambda x: getattr(transform, convert_type)(x[0], x[1])  # dynamic call convert func

            for fea in tqdm(source):
                if fea['geometry'] is None:
                    continue
                collections = fea['geometry']['coordinates']
                if type(collections) is tuple:
                    fea['geometry']['coordinates'] = f(collections)
                elif type(collections) is list:
                    fea['geometry']['coordinates'] = recur_map(f, collections)
                else:
                    raise TypeError("collection must be list or tuple")
                out.write(fea)


def getFileName(path):
    # 获取指定目录下的所有指定后缀的文件名
    path_list = []
    f_list = os.listdir(path)
    # print f_list
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.shp':
            path_list.append(i)
    return path_list


if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("-FilePath", "--path", required=True, help="转换文件的文件夹")
    ap.add_argument("-ConvertType", "--type", required=True, help="转换类型 支持 wgs2gcj bd2gcj")

    args = vars(ap.parse_args())

    # 遍历目录下的所有sharp文件
    convert_type = args["type"]

    plist = []
    # 目录
    path = args["path"]
    plist = getFileName(path)
    for item in plist:
        if not os.path.exists(path + "\\" + "OutPut"):
            os.mkdir(path + "\\" + "OutPut")
        dst_path = path + "\\OutPut\\" + os.path.splitext(item)[0] + '.shp'
        convertor(path + "\\" + item, dst_path, convert_type)
