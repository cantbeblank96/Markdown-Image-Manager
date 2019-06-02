import os
import shutil
import re
from downloader import supper_download
from file_control import get_relative_path, convert_path_to_standard_form

rule_url = re.compile(r"http[s]* *?: *?//.*")


def deal_with_image_links(image_links, file_old_path, file_new_path, image_new_folder,
                          b_convert_to_relative_path=True, b_download_web_image=True,
                          b_keep_original_img=True):
    """
    根据图片链接，将图片复制到image_new_folder文件夹中
    :b_download_web_image: 是否将网页图片下载到本地（默认是）
    :b_convert_to_relative_path: 是否将图片链接转换为相对路径（默认是）
    :b_keep_original_img: 保留原来的图片（默认是）
    file_new_path, file_old_path, image_new_folder 必须是绝对路径，而且是为 a/b/c 形式
    :return: image_new_links
    """

    file_old_folder, _ = os.path.split(file_old_path)
    file_new_folder, _ = os.path.split(file_new_path)

    # 将图片复制到folder_new文件夹中
    image_new_links = []
    for name, link in image_links:
        # url链接
        if rule_url.search(link):  # 判断是否为url链接
            if b_download_web_image:  # 下载url对应图片
                img_new_path = supper_download(link, image_new_folder)
            else:  # 保留原url
                image_new_links.append([name, link])
                continue
        # 本地链接
        else:
            link = link[1:] if link[0] == os.sep else link
            img_old_path = link if os.path.isabs(link) else os.path.join(file_old_folder, link)
            if os.path.exists(img_old_path):
                _, img_name = os.path.split(img_old_path)
                img_new_path = os.path.join(image_new_folder, img_name)
                if b_keep_original_img:
                    shutil.copy2(img_old_path, img_new_path)  # 复制文件到新路径
                else:
                    shutil.move(img_old_path, img_new_path)  # 移动文件（不建议）
            else:
                print("ERR: cant find img %s" % img_old_path)
                return []
        # 转化为相对路径
        if b_convert_to_relative_path:
            img_new_path = get_relative_path(file_new_folder, img_new_path)
        image_new_links.append([name, img_new_path])

    return image_new_links


def deal_with_image_folder_path(image_new_folder, b_path_type, file_new_path):
    """
    根据 file_new_path 来处理 image_new_folder
    :param image_new_folder: ""表示使用默认模式，不为空则使用正则模式处理
    :param b_path_type: image_new_folder路径的类型 {0:abs , 1:relative}
    :param file_new_path:
    :return: path, b_path_type(0/1), b_exist
    """
    # 处理 image_new_folder
    if not image_new_folder:  # 默认
        image_new_folder = os.path.splitext(file_new_path)[0]
    else:  # 正则
        image_new_folder = convert_path_to_standard_form(image_new_folder)
        # 用file_new_name替换掉[filename]关键字
        _, file_new_name = os.path.split(file_new_path)
        file_new_name, _ = os.path.splitext(file_new_name)  # 去除后缀
        split_ls = image_new_folder.split("[filename]")
        image_new_folder = split_ls[0]
        for pair in split_ls[1:]:
            image_new_folder += file_new_name
            image_new_folder += pair
        if b_path_type:  # 相对路径
            image_new_folder = os.path.join(os.path.split(file_new_path)[0], image_new_folder)
    return image_new_folder


if __name__ == '__main__':
    _image_new_folder = r"C:\Users\29118\Desktop\res\top\re_[filename]_fuck_you"
    _b_path_type = "1"
    _file_new_path = r"C:\Users\29118\Desktop\res\233.md"
    print(deal_with_image_folder_path(_image_new_folder, _b_path_type, _file_new_path))
