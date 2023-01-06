# -*- coding: utf-8 -*-

from ucloud.core import exc
from ucloud.client import Client
import logging

logger = logging.getLogger("ucloud")
logger.setLevel(logging.WARN)
import datetime
import re

public_key = "xxxxxxxxx"  # ucloud
private_key = "xxxxxxx"  # ucloud


def calc_last_x_day(days=7):
    today = datetime.date.today()
    seven_day = datetime.timedelta(days=days)
    seven_day = today - seven_day
    return seven_day.strftime("%Y%m%d")


today = datetime.date.today()

region = "cn-gd"
# region = "cn-bj2"
zones = {
    # "bj_B": "cn-bj2-02",
    # "bj_C" : "cn-bj2-03",
    # "bj_E" : "cn-bj2-05",
    "gz": "cn-gd-02"
}


def get_all_images(ProjectId, zone):
    client = Client({
        "project_id": ProjectId,
        "region": region,
        "public_key": public_key,
        "private_key": private_key,
        "base_url": "https://api.ucloud.cn"
    })

    try:
        resp = client.uhost().describe_image({
            "Zone": zone,
            "ImageType": "Custom",
            "Limit": 200

        })
    except exc.UCloudException as e:
        print(e)
    else:
        # print(resp)
        return resp.get("ImageSet")


def del_custom_image(ProjectId, image):
    client = Client({
        "project_id": ProjectId,
        "region": region,
        "public_key": public_key,
        "private_key": private_key,
        "base_url": "https://api.ucloud.cn"
    })
    try:
        resp = client.uhost().terminate_custom_image({
            "ImageId": image

        })
    except exc.UCloudException as e:
        print(e)
    else:
        print(resp)


def get_all_preject_id(public_key, private_key):
    client = Client({
        "public_key": public_key,
        "private_key": private_key,
        "base_url": "https://api.ucloud.cn"
    })

    try:
        resp = client.uaccount().get_project_list({
        })
    except exc.UCloudException as e:
        print(e)

    projects = resp.get("ProjectSet")
    for project in projects:
        ProjectId = project.get("ProjectId")
        yield ProjectId


def get_all_uhosts(ProjectId, Zone):
    global region
    client = Client({
        "project_id": ProjectId,
        "region": region,
        "Zone": Zone,
        "public_key": public_key,
        "private_key": private_key,
        "base_url": "https://api.ucloud.cn"
    })
    try:
        resp = client.uhost().describe_uhost_instance({
            "Zone": Zone,
            "project_id": ProjectId,
        })
        uhosts = resp.get("UHostSet")
        if len(uhosts) > 0:
            for uhost in uhosts:
                UHostId = uhost.get("UHostId")
                Name = uhost.get("Name")
                # print(UHostId,Name)
                yield UHostId, Name
    except exc.UCloudException as e:
        print(e)


def main():
    last_three_day = calc_last_x_day(3)
    print(last_three_day)
    project_ids = get_all_preject_id(public_key, private_key)
    for id in project_ids:
        for k, v in zones.items():
            uhosts = get_all_uhosts(id, v)  # 返回元组，uhost_id,name
            for uhost in uhosts:
                if re.search(r'uk8s.*', uhost[1]):
                    pass
                else:
                    # print(id,uhost[0],uhost[1])
                    images_name = uhost[1] + "_" + uhost[0] + "_" + last_three_day
                    print(images_name)
                    images = get_all_images(id, v)  # 拿到该区域的所有IMAGES。
                    # print(images)
                    for image in images:
                        ImageName = image.get("ImageName")
                        if ImageName == images_name:  # 根据 "主机名_主机id_日期" 找到对应的镜像
                            ImageId = image.get("ImageId")
                            del_custom_image(id, ImageId)


if __name__ == '__main__':
    main()
