import logging
import re

from ucloud.core import exc
from ucloud.client import Client

logger = logging.getLogger("ucloud")
logger.setLevel(logging.WARN)
import json
from loguru import logger
import datetime, time

logger.add("file_1.log", rotation="500 MB", level="ERROR")  # Automatically rotate too big file

today = datetime.date.today().strftime("%Y%m%d")  # 今天日期：2022-7-03


def get_yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday.strftime("%Y%m%d")


yesterday = get_yesterday()

##ucloud
public_key = "xxxxx"
private_key = "xxxxxx"

region = "cn-gd"
# region = "cn-bj2"
zones = {
    # "bj_B": "cn-bj2-02",
    # "bj_C" : "cn-bj2-03",
    # "bj_E" : "cn-bj2-05",
    "gz": "cn-gd-02"
}


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
                print(UHostId, Name)
                yield UHostId, Name


    except exc.UCloudException as e:
        print(e)


def make_image(ProjectId, Zone, UhostId, Name):
    global public_key
    global private_key
    global today
    global region
    client = Client({
        "region": region,
        "public_key": public_key,
        "private_key": private_key,
        "project_id": ProjectId,
        "base_url": "https://api.ucloud.cn"
    })

    try:
        resp = client.uhost().create_custom_image({
            "Zone": Zone,
            "UHostId": UhostId,
            "ImageName": str(Name) + "_" + str(UhostId) + "_" + str(today)  # 名称web_server_uhost-wdgqbtgr_20220721

        })
    except exc.UCloudException as e:
        print(e)
    else:
        print(resp)


def main():
    project_ids = get_all_preject_id(public_key, private_key)
    for id in project_ids:
        for k, v in zones.items():
            uhosts = get_all_uhosts(id, v)  # 返回元组，uhost_id,name
            for uhost in uhosts:
                if re.search(r'uk8s.*', uhost[1]):
                    pass
                else:
                    make_image(id, v, uhost[0], uhost[1])


if __name__ == '__main__':
    main()
