import sys
import pathlib
import shutil

# <EXTENTIONS> dictionary with new folders names(<keys>)
# and file extensions (<values>) which should be mowed
# to these folders

EXTENSIONS = {
    "images": ('.jpeg', '.jpg', '.gif', '.JPG', '.png', '.CR2', '.svg'),
    "documents": ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx'),
    "video": ('.avi', '.mp4', '.mov', '.mkv', '.mpeg', '.mpg', '.wmv'),
    "audio": ('.mp3', '.aac', '.wav', '.flac', '.m3u', '.wma'),
    "archives": ('.zip', '.tar', '.gz')
}

# <main> function <main> checks if the path to the Directory
# to clean there is correct


def main():
    global main_folder
    if len(sys.argv) < 2:
        user_input = input('Please enter path to directory: ')
    else:
        user_input = sys.argv[1]
    while True:
        main_folder = pathlib.Path(user_input)
        if main_folder.exists():
            if main_folder.is_dir():
                break
            else:
                user_input = input(
                    'This is file name. Enter path to directory: ')
        else:
            user_input = input(
                f'Such <{main_folder}> does not exist. Enter path to directory: ')
    browse_files(main_folder)


# <browse_files> function
# - looks over all files in folders of the Directory proposed.
# (Path to that Directory we've got from the <main> function)
# - renames folders (transliteration) using <normalize> function
# - delete empty folders

def browse_files(folder):
    for item in folder.iterdir():
        if item.is_file():
            file = item
            move_files(file)

        elif item.name not in EXTENSIONS:
            if not any(folder.iterdir()):
                folder.rmdir()
                continue
            new_item_name = normalize(item.name.removesuffix(item.suffix))
            new_path_item = folder.joinpath(new_item_name + item.suffix)
            new_item = item.rename(new_path_item)
            subfolder = new_item
            browse_files(subfolder)

            if not any(subfolder.iterdir()):
                subfolder.rmdir()


# <move_file> function
# - renames files and folders (transliteration) using <normalize> function
# - moves these files to the new folders with names specified in <EXTENTIONS> dictionary.
# - ads folders where to extract files from archives (folders names are the same as
# the archives names)
# - unpack the files from archives
# - delete the archive files

def move_files(file):
    for nam, ext in EXTENSIONS.items():
        if file.suffix in ext:
            new_folder = main_folder.joinpath(nam)
            new_folder.mkdir(exist_ok=True)
            new_file_name = normalize(file.name.removesuffix(file.suffix))
            new_path_file = new_folder.joinpath(new_file_name + file.suffix)
            try:
                new_file = file.rename(new_path_file)
            except FileExistsError:
                new_file = file.replace(new_path_file)
                break
            if nam == 'archives':
                archive_folder = new_folder.joinpath(
                    new_file.name.removesuffix(file.suffix))
                archive_folder.mkdir(exist_ok=True)
                shutil.unpack_archive(new_file, archive_folder)
                new_file.unlink(missing_ok=True)
            break

# <normalize> function makes transliteration of the file/folder names:
# - replace Cyrillic symbols on latin
# - replace other symbols ex??ept digits and Latin on symbol "_"
# - ads ending "_copy" to the files with the same names


def normalize(file, is_copy=False):
    map = {'??': 'a', '??': 'b', '??': 'v', '??': 'g', '??': 'd', '??': 'e', '??': 'e', '??': 'zh', '??': 'z', '??': 'i', '??': 'y',
           '??': 'k', '??': 'l', '??': 'm', '??': 'n', '??': 'o', '??': 'p', '??': 'r', '??': 's', '??': 't', '??': 'u', '??': 'f', '??': 'h',
           '??': 'ts', '??': 'ch', '??': 'sh', '??': 'sch', '??': '', '??': 'y', '??': '', '??': 'e', '??': 'yu', '??': 'ya', '??': 'i',  '??': 'e', '??': 'i', '??': 'A',
           '??': 'B', '??': 'V', '??': 'G', '??': 'D', '??': 'E', '??': 'E', '??': 'Zh', '??': 'Z', '??': 'I', '??': 'Y', '??': 'K', '??': 'L',
           '??': 'M', '??': 'N', '??': 'O', '??': 'P', '??': 'R', '??': 'S', '??': 'T', '??': 'U', '??': 'F', '??': 'H', '??': 'Ts', '??': 'Ch',
           '??': 'Sh', '??': 'Sch', '??': '', '??': 'Y', '??': '', '??': 'E', '??': 'Yu', '??': 'Ya', '??': 'I',  '??': 'E',  '??': 'I'}
    new_name = ''
    for el in file:
        if el in map:
            new_name += map[el]
        elif (ord('A') <= ord(el) <= ord('Z')) or (ord('a') <= ord(el) <= ord('z')) or el.isdigit():
            new_name += el
        else:
            new_name += '_'
    if is_copy:
        new_name += '_copy'
    return new_name


if __name__ == '__main__':
    main()
