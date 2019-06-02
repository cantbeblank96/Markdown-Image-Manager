# Markdown-Image-Manager

[英文版请点击这里](README_EN.md)

让复制markdown文件的同时也带上图片。
支持批量复制，和路径正则匹配。
还有更多高级功能等待你去探索哦！

Copy/Move the markdown file along with the image.
Support for batch copy, and path regular matching .
There are more advanced features for you to explore!

如果这个软件能够解决你的问题，请给我一个**小星星**。 <(▰˘◡˘▰)> 
欢迎提出建议。

If this software can solve your problem, please give me a **star**. 
Suggestions are welcome.

## 项目结构

- src：源码
- dist：发行版exe软件，仅支持Windows。对于其他系统，请直接下载src，然后用python3运行里面的main.py即可。
- README.md：中文版介绍
- README_EN.md：英文版介绍

## 为什么要开发这个软件？

Typora是一款优秀的Markdown编辑器，它支持图片拖拽、复制粘贴的操作，并且能自动拷贝你指定的目录下。

![1559480154722](README\1559480154722.png)

比如我常用的就是最后一个选项，它将在你的markdown文件（以Trump_is_idiot.md为例）的同一目录下，生成一个{filename}.assert文件夹（也就是Trump_is_idiot.assert）来存放使用到的图片。

一般来说，这已经足够方便。但是在实际使用中，我遇到了以下问题：

- 对于以前的旧文件（当时Typora的图片插入功能并没有这么智能），并没有一个文件夹来集中存放图片，文件中的图片链接既有本地的相对链接、绝对链接，也有网络上的url链接。

  很不幸地，这很容易导致图片丢失，比如：刚好使用了暂存区的图片然后你手贱清空了暂存区（默哀），又或者是网上的url失效了。 (╯￣Д￣)╯╘═╛ 

- Typora现在的图片插入只支持三种方式，分别是：拷贝到自己指定的某个文件夹（不方便）、拷贝到当前目录下的assets文件夹、拷贝到{filename}.assert文件夹。这非常具有局限性。

  比如我用来搭建博客的hexo要求，文件{filename}.md的图片必须放到{filename}文件夹下。这是上面提到的三种方式所满足不了的。当然可以先用{filename}.assert，然后将.assert替换掉，但是这样做相当麻烦！  (╯￣Д￣)╯╘═╛ 

## 软件的基本功能

>以下为代号意义：
>file_source.md: 源markdown文件
>file_new.md: 新生成的markdown文件，文件名将由你设定
>image_new_folder: 用来存放file_new.md中引用的图片的文件夹

它是如何完成markdown文件的带图片复制的？

- 首先，从file_source.md中找出所有图片链接；
- 然后，根据图片链接，将图片复制到image_new_folder文件夹中；
- 接着，从file_source.md复制一份副本file_new.md（如果file_new与file_source一致，则跳过该步）；
- 最后，将file_new.md中的图片链接对应地修改为，指向image_new_folder文件夹中的图片。

## 使用方法

### 模式选择

分6个阶段选择工作模式：

```
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
```

！！注意！！

在Step 2nd输入image_new_folder时，如果输入不为空，将使用正则模式处理输入：

```
（1）默认(直接回车确认)
默认为与 file_new_path 在同一路径下的同名文件夹, such as:
file_new_path : file_new_folder/xxx.md
image_new_folder : file_new_folder/xxx
（2）正则
可以为绝对路径或者相对路径，将会把路径中的[filename]关键字替换为file_new_name, such as:
when file_new_path is ~/here/Markdown.md
绝对路径 : ~/29118/my/res/pic_[filename]_233 ==> ~/29118/my/res/pic_Markdown_233
相对路径 : abc/pic_[filename]_233 ==> ~/here/abc/res/pic_Markdown_233
```



### 使用演示

就以我用来存放博客的文件夹为例：

![1559482186895](README\1559482186895.png)

markdown中用到的**部分**图片存放在top文件夹下的__{filename}.assert文件夹中，其他则为url链接。

![1559482246418](README\1559482246418.png)

![1559482358598](README\1559482358598.png)

#### 1.将其转换为hexo的默认格式

由于是对整个文件夹下的文件进行操作，输入1选择Folder模式。

![1559482787434](README\1559482787434.png)

根据提示依次输入路径，image_new_folder使用了正则模式。

![1559484001247](README\1559484001247.png)

后面几步都按回车键，选择默认模式即可。

![1559483086948](README\1559483086948.png)

运行结果：

![1559483115579](README\1559483115579.png)

完美！~ ＼( ^▽^ )／ 

#### 2.恢复回去

那能不能将上面转换过来的hexo格式目录，恢复成原来的目录结构呢？Of course, we can！

我先把源文件夹清空。

![1559483370602](README\1559483370602.png)

还是用文件夹模式。

![1559483412657](README\1559483412657.png)

注意看各个路径。

![1559483538808](README\1559483538808.png)

一直按回车，我们就得到结果了：

![1559484026126](README\1559484026126.png)

![1559484038660](README\1559484038660.png)

![1559484046862](README\1559484046862.png)

完美！~ (/≧▽≦)/

## 关于源码的进一步介绍

### 源码中的路径

```
绝对路径: file_old_path, file_new_path, file_old_folder, file_new_folder
可以为相对路径 或 绝对路径: image_new_folder

file_old_path 或 file_old_folder 为必要项，其他为可选项（可直接回车跳过）

file_new_path 默认与 file_old_path 相同
file_new_folder 默认与 file_old_folder 相同

image_new_folder 就有点复杂了，就像上面说的分为默认模式与正则模式
```

我在源码中的注释还是挺详细的，请直接看源码吧。