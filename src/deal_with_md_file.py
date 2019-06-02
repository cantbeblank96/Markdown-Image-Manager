import re

rule_img_lk = re.compile(r"!\[(.*?)\]\((.+?)\)")  # ![pic_name](pic_link)


def find_image_links_from_content(content):
    """从markdown_file的内容中找出所有图片链接"""

    if content:
        image_links = rule_img_lk.findall(content)  # image_links:[('pic_name','pic_link')]
        return image_links
    else:
        return []


rule_img_lk_without_group = re.compile(r"!\[.*?\]\(.+?\)")  # ![pic_name](pic_link)


def replace_old_image_links_with_the_new(content, image_new_links):
    """用新的image_links替换掉旧的image_links"""

    content_split_ls = rule_img_lk_without_group.split(content)
    if len(image_new_links) != len(content_split_ls) - 1:
        print("ERR: image_links length(%s) doesn't match" % len(image_new_links))
        return None
    content_new = content_split_ls[0]
    for i in range(len(image_new_links)):
        link = image_new_links[i]
        content_new += "![%s](%s)" % (link[0], link[1])
        content_new += content_split_ls[i + 1]
    return content_new


if __name__ == '__main__':
    from file_control import read_markdown

    folder = r'E:\pycharm_source\markdown图片管家\test'
    file_name = r'markdown语法.md'
    content_ = read_markdown(folder, file_name)
    print(content_[350:460])
    image_links_ = find_image_links_from_content(content_)
    print(image_links_)
