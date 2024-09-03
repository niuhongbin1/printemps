import os
from typing import Union
import stat

def clean_folder(folder_path: Union[str, list[str]]):
    """Remove all files and folders within the folder_path.

    :param folder_path:
    :return:
    """
    if isinstance(folder_path, str):
        folder_path = [folder_path]

    for folder in folder_path:
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                file_name = os.path.join(root, name)
                try:
                    os.unlink(file_name)
                except PermissionError:
                    # 某些只读文件删不掉，需要先赋予 写 的权限，然后再删除
                    os.chmod(file_name, stat.S_IWRITE)
                    try:
                        os.unlink(file_name)
                    except Exception:
                        pass
            for name in dirs:
                # 某些文件夹也删除不掉，譬如U盘的系统文件夹（保存U盘自身信息的文件夹）
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception:
                    pass



if __name__ == '__main__':
    clean_folder('../res')