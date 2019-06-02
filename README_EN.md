# Markdown-Image-Manager

[Chinese version](README.md)

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

## Project Structure

- src: source code
- dist: The release exe software only supports Windows. For other systems, please download the src folder directly, then run main.py inside python3.
- README.md: Chinese version
- README_EN.md: English version

## Why develop this software?

Typora is an excellent Markdown editor that supports drag and drop, copy and paste operations, and automatically copies images to your specified directory.

![1559480154722](README_EN/1559480154722.png)

For example, the one that I use is the last option. It will generate a {filename}.assert folder in the same directory of your markdown file to store the used image.(for example, Trump_is_idiot.md and Trump_is_idiot.assert)

Generally speaking, this is convenient enough. But in actual use, I have encountered the following problems:

- For the old files (Typora's image insertion function was not so smart at the time), there is no folder to store the images centrally. The image links in the file have local relative links, absolute links, and url links on the network. .

  Unfortunately, this can easily lead to the loss of images, such as: just use the image of the temporary storage area and then you empty the temporary storage area (silence), or the online url is invalid. (╯￣Д￣)╯╘═╛ 

- Typora's current image insertion supports only three methods: copy to a folder you specify (inconvenient), copy to the assets folder in the current directory, and copy to the {filename}.assert folder. This is very limited.

  For example, the hexo that I used to build the blog, request the image of the file {filename}.md must be placed in the {filename} folder. This is not in the three ways mentioned above. Of course you can use {filename}.assert first, then replace .assert, but this is quite troublesome!  (╯￣Д￣)╯╘═╛ 

## Basic functions of the software

>The following are the meaning of the variables:
>file_source.md: source markdown file
>file_new.md: newly generated markdown file, the file name will be set by you
>image_new_folder: The folder used to store the images referenced in file_new.md

How does it work?

- First, find out all image links from file_source.md;
- Then, according to the image link, copy the image to the image_new_folder folder;
- Next, copy a copy of file_new.md from file_source.md (if file_new is consistent with file_source, skip this step);
- Finally, modify the image link in file_new.md to point to the image in the image_new_folder folder.

## How to use

### Steps for usage

A total of 6 stages：

```
Step 1st -- choose File mode ：Specify a file to process, the output is also a file
         |
         -- choose Folder mode ：Specify a folder and process its next series of files, the output is a folder

            (File mode)
Step 2nd -- Enter the path as prompted ：file_old_path, (file_new_path, image_new_folder(default mode or regular mode))
         |
         |  (Folder mode)
         -- Enter the path as prompted ：file_old_folder, (file_new_folder, image_new_folder(( default mode or regular mode))
         
(Folder mode)
Step 3rd -- preserve file structure ：such as file_old_folder/b/c/xxx.md ==>  file_new_folder/b/c/xxx.md
         |
         -- ignore structure ：such as file_old_folder/b/c/xxx.md ==>  file_new_folder/xxx.md
         
Step 4th -- copy img ：Keep the original file
         |
         -- move img ：Do not retain original files
         
Step 5th -- download web img
         |
         -- keep url
         
Step 6th -- Want the new image links to be absolute or relative? Yes
         |
         -- No
```

**！！Note！！**

**When entering image_new_folder in Step 2nd, if the input is not empty, the input will be processed using regular mode:**

```
(1) default mode (carriage return)
Image_new_folder defaults to the same name folder in the same path as file_new_path, such as:
File_new_path : file_new_folder/xxx.md
Image_new_folder : file_new_folder/xxx
(2) Regular mode
Can be an absolute path or a relative path, which will replace the [filename] keyword in the path with file_new_name, such as:
When file_new_path is ~/here/Markdown.md
Absolute path : ~/29118/my/res/pic_[filename]_233 ==> ~/29118/my/res/pic_Markdown_233
Relative path: abc/pic_[filename]_233 ==> ~/here/abc/res/pic_Markdown_233
```



### Demonstration

Take the folder I used to store my blog as an example:

![1559482186895](README_EN\1559482186895.png)

Some of the images used in the markdown file are stored in the __{filename}.assert folder in the top folder, and the others are url links.

![1559482246418](README_EN\1559482246418.png)

![1559482358598](README_EN\1559482358598.png)

#### 1.Convert it to the default directory format for hexo

Enter 1 to select the Folder mode.

![1559482787434](README_EN\1559482787434.png)

Enter the path as prompted. Image_new_folder uses regular mode.

![1559484001247](README_EN\1559484001247.png)

Press the Enter key in the next few steps to select the default mode.

![1559483086948](README_EN\1559483086948.png)

result:

![1559483115579](README_EN\1559483115579.png)

perfect！~ ＼( ^▽^ )／ 

#### 2.Restore back

Can it be restored to the original directory structure by converting the directory that matches the hexo format? 
Of course, we can！

I first clear the source folder.

![1559483370602](README_EN\1559483370602.png)

Still use the folder mode.

![1559483412657](README_EN\1559483412657.png)

Look at the various paths.

![1559483538808](README_EN\1559483538808.png)

Keep pressing Enter, we get the results:

![1559484026126](README_EN\1559484026126.png)

![1559484038660](README_EN\1559484038660.png)

![1559484046862](README_EN\1559484046862.png)

perfect！~ (/≧▽≦)/

## Further introduction to the source code

### Path variable

```
Absolute path: file_old_path, file_new_path, file_old_folder, file_new_folder
Can be a relative path or an absolute path: image_new_folder

file_old_path or file_old_folder is required

file_new_path defaults to file_old_path
file_new_folder defaults to file_old_folder

image_new_folder is a bit complicated, as described above, divided into default mode and regular mode.
```

My comments in the source code are quite detailed, please try to use the Google Translate to see the source code comments.
