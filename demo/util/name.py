import uuid


def mkOriginImgName(filename):
    """为上传的图片生成文件名"""
    file_type = filename.split('.')[-1]
    pre_name = str(uuid.uuid1())
    return 'img' + pre_name + '.' + file_type
