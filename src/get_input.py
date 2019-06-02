import os
from file_control import convert_path_to_standard_form


def get_input_mode(mode_description_ls, input_tips=None):
    """
    获取输入，并根据 mode_description_ls 返回选择的 mode
    :param mode_description_ls: 第一个item为默认模式 [[mode, description], ……]
    description 为对应的输入
    :param input_tips: 不设定时将根据 mode_description_ls 自动生成
    """

    description_mode_dict = {str(description): str(mode) for mode, description in mode_description_ls}
    if not input_tips:
        input_tips = "pls choose %s(%s|default)" % (mode_description_ls[0][0], mode_description_ls[0][1])
        for mode, description in mode_description_ls[1:]:
            input_tips += "/%s(%s)" % (mode, description)
        input_tips += " mode:\n"
    while True:
        input_str = input(input_tips)
        try:
            if not input_str:  # 输入""使用默认值
                mode = str(mode_description_ls[0][0])
            else:
                mode = description_mode_dict.get(input_str, None)
                if mode is None:
                    print("ERR:input value exceeds range!")
                    continue
            print("Mode %s is selected" % mode)
            break
        except Exception as e:
            print(Exception, ":", e)
    return mode


def get_input_path(b_path_type=0, b_need_exist=True, b_file_or_folder=2, input_tips=None):
    """
    获取输入的 path
    :param b_path_type: {0:need to be abs path, 1:need to be relative path, 2:whatever}
    :param b_need_exist: need to be exist path
    :param b_file_or_folder: {0:need to be file, 1:need to be folder, 2:whatever}
    :param input_tips: 默认将根据选择的 b_path_type 和 b_need_exist 自动生成
    :return: path, b_path_type(0/1), b_exist
    """

    if not input_tips:
        input_tips = "pls enter %s path" % {0: "absolute", 1: "relative", 2: "absolute or relative"}.get(b_path_type)
        if b_need_exist:
            input_tips += "(need to exist)"
        input_tips += ":\n"
    while True:
        input_str = input(input_tips)
        try:
            # b_need_exist
            b_exist = os.path.exists(input_str)
            if b_need_exist and not b_exist:
                print("ERR:Path does not exist")  # 路径不存在
                continue

            # 默认值
            if not input_str:  # 输入""使用默认值
                print("use default path")
                return input_str, 2, False, 2

            # b_path_type
            if os.path.isabs(input_str):  # 是绝对路径
                if b_path_type in [0, 2]:
                    b_path_type = 0
                else:
                    print("ERR:expect relative path, but get absolute path")
                    continue
            else:  # 相对路径
                if b_path_type in [1, 2]:
                    b_path_type = 1
                else:
                    print("ERR:expect absolute path, but get relative path")
                    continue

            # b_file_or_folder
            if os.path.splitext(input_str)[1]:  # 是file
                if b_file_or_folder in [0, 2]:
                    b_file_or_folder = 0
                else:
                    print("ERR:expect folder, but get file")
                    continue
            else:  # 是folder
                if b_file_or_folder in [1, 2]:
                    b_file_or_folder = 1
                else:
                    print("ERR:expect file, but get folder")
                    continue

            print("get path : %s" % input_str)
            return input_str, b_path_type, b_exist, b_file_or_folder
        except Exception as e:
            print(Exception, ":", e)


def get_input():
    """获取输入（总接口）"""

    # Step 1st: choose File/Folder mode
    print("Step 1st: choose mode")
    mode_description_ls = [["File", "0"], ["Folder", "1"], ["Quit", "q"]]
    mode = get_input_mode(mode_description_ls)

    # Step 2nd: Enter path
    print("\nStep 2nd: pls enter the path as prompted")
    file_old_path, file_new_path, file_old_folder, file_new_folder = "", "", "", ""
    if mode == "Quit":  # 退出
        print("Exiting program.....\n")
        return [None] * 7
    elif mode == "File":  # File mode 文件模式
        # file_old_path
        print("file_old_path: where the source markdown files in")
        file_old_path, _, _, _ = get_input_path(b_path_type=0, b_need_exist=True, b_file_or_folder=0)
        file_old_path = convert_path_to_standard_form(file_old_path)

        # file_new_path
        print("file_new_path: result file path, default as same as file_old_path")
        file_new_path, b_path_type, _, _ = get_input_path(b_path_type=2, b_need_exist=False, b_file_or_folder=0)
        if not file_new_path:
            file_new_path = file_old_path
        else:
            file_new_path = convert_path_to_standard_form(file_new_path)
            if b_path_type:  # 相对路径
                file_new_path = os.path.join(os.path.split(file_old_path)[0], file_new_path)

    elif mode == "Folder":  # Folder mode 文件夹模式
        # file_old_folder
        print("file_old_folder: source folder path")
        file_old_folder, _, _, _ = get_input_path(b_path_type=0, b_need_exist=True, b_file_or_folder=1)
        file_old_folder = convert_path_to_standard_form(file_old_folder)

        # file_new_folder
        print("file_new_folder: result folder path, default as same as file_old_folder")
        file_new_folder, b_path_type, _, _ = get_input_path(b_path_type=2, b_need_exist=False, b_file_or_folder=1)
        if not file_new_folder:
            file_new_folder = file_old_folder
        else:
            file_new_folder = convert_path_to_standard_form(file_new_folder)
            if b_path_type:  # 相对路径
                file_new_folder = os.path.join(file_new_folder, file_new_folder)

    # image_new_folder
    print("image_new_folder: a folder for storing imgs")
    image_new_folder, b_path_type_img_folder, _, _ = get_input_path(b_path_type=2, b_need_exist=False,
                                                                    b_file_or_folder=2)
    # 暂不处理，后面再根据不同的 file_new_path 来处理

    # Step 3rd: (Folder mode)file structure
    if mode == "Folder":
        print("\nStep 3rd: pls select whether to retain the file structure")
        structure_mode_description_ls = [["preserve", "0"], ["ignore", "1"]]
        b_keep_structure = True if get_input_mode(structure_mode_description_ls) == "preserve" else False
    else:
        b_keep_structure = None

    # Step 4th: copy/move img
    print("\nStep 4th: pls select how the picture moves")
    mode_description_ls = [["copy", "0"], ["move", "1"]]
    b_keep_original_img = True if get_input_mode(mode_description_ls) == "copy" else False

    # Step 5th:
    print("\nStep 5th: Want to download web images?")
    mode_description_ls = [["yes", "1"], ["no", "0"]]
    b_download_web_image = True if get_input_mode(mode_description_ls) == "yes" else False

    # Step 6th:
    print("\nStep 6th: Want the new image links to be absolute or relative?")
    mode_description_ls = [["relative", "1"], ["absolute", "0"]]
    b_convert_to_relative_path = True if get_input_mode(mode_description_ls) == "relative" else False

    # return
    if mode == "File":  # File mode 文件模式
        return mode, file_old_path, file_new_path, image_new_folder, \
               b_path_type_img_folder, b_keep_structure, \
               b_keep_original_img, b_download_web_image, b_convert_to_relative_path
    elif mode == "Folder":  # Folder mode 文件夹模式
        return mode, file_old_folder, file_new_folder, image_new_folder, \
               b_path_type_img_folder, b_keep_structure, \
               b_keep_original_img, b_download_web_image, b_convert_to_relative_path


if __name__ == '__main__':
    # mode, file_old_path, file_new_path, image_new_folder, b_path_type_img_folder, mode_structure, mode_img_move = get_input()
    print(get_input())
    pass
