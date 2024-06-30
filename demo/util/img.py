from server.settings import PATH_TYPE, SERVER_PATH, IMG_DOWNLOAD_PATH, SAVE_DIR


def transPath(path, path_type) -> str:
    """将URL与本地路径互换"""
    img_name = str(path).split('/')[-1]
    print(">>> transPath::", img_name)
    if path_type == PATH_TYPE['URL']:
        return SAVE_DIR + img_name
    if path_type == PATH_TYPE['LOCAL']:
        return SERVER_PATH + IMG_DOWNLOAD_PATH + img_name

