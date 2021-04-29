# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:


def pytest_collection_modifyitems(items):
    """
    Transform unicode into utf-8 on the console.
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")