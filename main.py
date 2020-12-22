#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author: AimerNeige
# Site: https://aimerneige.com
# Mail: aimer.neige.soft@gmail.com

import requests
import subprocess
import json
import sys


def get_json(mid:'int', ps:'int', pn:'int') -> 'str':
    """
    Get json data from bilibili api
    :param mid:  user id
    :param  ps:  item number per page
    :param  pn:  current page
    :return str: json data
    """

    url = "http://api.bilibili.com/x/space/arc/search?mid=%d&ps=%d&pn=%d" % (mid, ps, pn)
    response = requests.get(url)
    assert response.status_code == 200, "Request failed!"
    response.encoding = 'utf-8'
    json_data = response.text
    return json_data


def get_bv_id(json_data:'str') -> 'list':
    """
    Get all BV id from json data
    "param  json_data: json data
    :return list:      list of bvid
    """
    bv_id_list = []
    obj = json.loads(json_data)
    video_list = obj['data']['list']['vlist']
    for video in video_list:
        bv_id_list.append(video["bvid"])
    return bv_id_list


def download_video(url:'str'):
    """
    Call an subprogress and download video with `you-get`
    :param url: Video url of bilibili
    :return: None
    """
    print("Start Download %s" % (url))
    subprocess.call("you-get %s" % (url), shell=True)


def print_help():
    # Just simply print help menu
    help_str = """
Run this with a bilibii user space url, like this:
    `python3 main.py https://space.bilibili.com/13081489`
Or you can just give the uid, like this:
    `python3 main.py 13081489`"""
    print(help_str)


def main():
    # Main function
    sys_argv = sys.argv
    sys_argc = len(sys_argv)
    mid = 13081489
    pn = 1
    ps = 100
    if sys_argc == 1:
        print("Please give more argument!")
        print_help()
        exit()
    elif sys_argc == 2:
        try:
            int(sys_argv[1])
        except:
            try:
                int(sys_argv[1].split('/')[3])
            except:
                print("Wrong Argument, please check your url.")
                print_help()
                exit()
            else:
                mid = int(sys_argv[1].split('/')[3])
        else:
            mid = int(sys_argv[1])
        finally:
            count = int(json.loads(get_json(mid, ps, pn))['data']['page']['count'])
            pages = int(count / ps + 1)
            for i in range(1, pages + 1):
                json_data = get_json(mid, ps, i)
                bv_id_list = get_bv_id(json_data)
                for bv_id in bv_id_list:
                    download_video("https://www.bilibili.com/video/%s" % (bv_id))
    else:
        print("Wrong Argument!")
        print_help()
        exit()


if __name__ == "__main__":
    main()
