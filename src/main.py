from file_control import read_markdown, write_markdown, make_folder, search_file_flat
from deal_with_md_file import find_image_links_from_content, replace_old_image_links_with_the_new
from deal_with_image import deal_with_image_links, deal_with_image_folder_path
from get_input import get_input
import os

# 功能介绍：
"""
以下为代号意义：
file_source.md: 源markdown文件
file_new.md: 新生成的markdown文件，文件名将由你设定
image_new_folder: 用来存放file_new.md中引用的图片的文件夹


功能：
“完成markdown文件的带图片复制”
首先，从file_source.md中找出所有图片链接；
然后，根据图片链接，将图片复制到image_new_folder文件夹中；
接着，从file_source.md复制一份副本file_new.md（如果file_new与file_source一致，则跳过该步）；
最后，将file_new.md中的图片链接对应地修改为，指向image_new_folder中的图片。
"""

# 模式选择：
"""
分6个阶段选择工作模式：

Step 1st -- choose File mode 文件模式：指定某个文件进行处理，输出也是文件
         |
         -- choose Folder mode 文件夹模式：指定某个文件夹，对其下一系列文件进行处理，输出是一个文件夹

            (File mode)
Step 2nd -- Enter the path as prompted 根据提示输入路径：file_old_path, (file_new_path, image_new_folder(默认、正则))
         |
         |  (Folder mode)
         -- Enter the path as prompted 根据提示输入路径：file_old_folder, (file_new_folder, image_new_folder(默认、正则))
         
(Folder mode)
Step 3rd -- preserve file structure 保留文件结构：such as file_old_folder/b/c/xxx.md ==>  file_new_folder/b/c/xxx.md
         |
         -- ignore structure 不保留文件结构：such as file_old_folder/b/c/xxx.md ==>  file_new_folder/xxx.md
         
Step 4th -- copy img 复制本地图片：Keep the original file
         |
         -- move img 移动本地图片：Do not retain original files
         
Step 5th -- download web img 下载网络图片
         |
         -- keep url 不下载
         
Step 6th -- Want the new image links to be absolute or relative? Yes
         |
         -- No        
"""

# 路径输入：
"""
绝对路径: file_old_path, file_new_path, file_old_folder, file_new_folder
可以为相对路径 或 绝对路径: image_new_folder

file_old_path 或 file_old_folder 为必要项，其他为可选项（可直接回车跳过）

file_new_path 默认与 file_old_path 相同
file_new_folder 默认与 file_old_folder 相同

image_new_folder 就有点复杂了：
（1）默认(直接回车确认)
默认为与 file_new_path 在同一路径下的同名文件夹, such as:
file_new_path : file_new_folder/xxx.md
image_new_folder : file_new_folder/xxx
（2）正则
可以为绝对路径或者相对路径，将会把路径中的[filename]关键字替换为file_new_name, such as:
when file_new_path is ~/here/Markdown.md
绝对路径 : ~/29118/my/res/pic_[filename]_233 ==> ~/29118/my/res/pic_Markdown_233
相对路径 : abc/pic_[filename]_233 ==> ~/here/abc/res/pic_Markdown_233        
"""


def steward(file_old_path, file_new_path, image_new_folder,
            b_convert_to_relative_path=True, b_download_web_image=True,
            b_keep_original_img=True):
    """图片管家的基本操作"""

    # 安全锁：建立/检查文件夹
    file_new_folder, _ = os.path.split(file_new_path)
    try:
        make_folder(image_new_folder, file_new_folder)
    except Exception as e:
        print("failed to make folders %s or %s" % (file_new_folder, image_new_folder))
        print(Exception, ":", e)
        return False

    content = read_markdown(file_old_path)
    image_links = find_image_links_from_content(content)
    image_new_links = deal_with_image_links(image_links, file_old_path, file_new_path, image_new_folder,
                                            b_convert_to_relative_path=b_convert_to_relative_path,
                                            b_download_web_image=b_download_web_image,
                                            b_keep_original_img=b_keep_original_img)
    content_new = replace_old_image_links_with_the_new(content, image_new_links)
    write_markdown(content_new, file_new_path)
    return True


def main():
    # 模式选择
    mode, file_old_, file_new_, image_new_folder, \
    b_path_type_img_folder, b_keep_structure, \
    b_keep_original_img, b_download_web_image, b_convert_to_relative_path = get_input()

    file_old_path_ls, file_new_path_ls, image_new_folder_ls = [], [], []

    if mode == "Folder":
        file_old_folder, file_new_folder = file_old_, file_new_
        file_old_path_ls = search_file_flat(file_old_folder, suffix_ls=[".md"], flag_ls=None, case_sensitive=False)
        for file_old_path in file_old_path_ls:
            if b_keep_structure:
                # file_old_folder/b/c/xxx.md ==>  file_new_folder/b/c/xxx.md
                file_new_path = file_new_folder + file_old_path.split(file_old_folder)[1]
            else:
                # file_old_folder/b/c/xxx.md ==>  file_new_folder/xxx.md
                file_new_path = os.path.join(file_new_folder, os.path.split(file_old_path)[1])
            image_new_folder_trans = deal_with_image_folder_path(image_new_folder, b_path_type_img_folder, file_new_path)
            file_new_path_ls.append(file_new_path)
            image_new_folder_ls.append(image_new_folder_trans)

    elif mode == "File":
        file_old_path, file_new_path = file_old_, file_new_
        image_new_folder_trans = deal_with_image_folder_path(image_new_folder, b_path_type_img_folder, file_new_path)
        file_old_path_ls.append(file_old_path)
        file_new_path_ls.append(file_new_path)
        image_new_folder_ls.append(image_new_folder_trans)

    # print(file_old_path_ls)
    # print(file_new_path_ls)
    # print(image_new_folder_ls)
    for i in range(len(file_new_path_ls)):
        steward(file_old_path_ls[i], file_new_path_ls[i], image_new_folder_ls[i],
                b_convert_to_relative_path, b_download_web_image,
                b_keep_original_img)

    print("\nCongratulations, accomplished!\nThe output path is %s\n\n(/≧▽≦)/\n" % file_new_)


if __name__ == '__main__':
    # C:\Git\My_git_blog\my_blog\source
    # file_old_path = r'E:\pycharm_source\markdown图片管家\test\markdown语法.md'
    # file_new_path = r"C:\Users\29118\Desktop\res\233.md"
    # image_new_folder = r"C:\Users\29118\Desktop\res\233"
    # steward(file_old_path, file_new_path, image_new_folder)
    while True:
        main()
        input_str = input("continue? yes(1|default)/no(0)")
        if input_str != "0":
            continue
        else:
            break
    # top\__[filename].assert
