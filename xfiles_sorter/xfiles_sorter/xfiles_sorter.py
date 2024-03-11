import os
import shutil
import zipfile
import logging


def normalize(file_name):
    translit_table = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
        'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'iu', 'я': 'ia'
    }

    result = ''
    base_name, extension = os.path.splitext(file_name)
    for char in base_name:
        result += translit_table.get(char, char) if char not in ['/', '\\'] else char
    return result + extension


def remove_empty_folders(folder_path):
    folder_removed = False
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            current_folder = os.path.join(root, directory)
            try:
                os.rmdir(current_folder)
                print(f"Folder Purged of Contents: {current_folder}")
                folder_removed = True
            except OSError as e:
                # Error message printing removed to not display non-empty folder errors
                pass
    if not folder_removed:
        print("No Confidential Folders Detected.")


def organize_files(folder_path, target_folder_path):
    logging.basicConfig(filename='organize_files.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    if not target_folder_path:
        target_folder_path = folder_path
    
    folders_to_ignore = ['archived intel', 'classified footage', 'covert audio', 'top-secret documents', 'sensitive imager', 'miscellaneous classified data']
    files_moved_count = {category: 0 for category in folders_to_ignore}

    for folder in folders_to_ignore:
        target_path = os.path.join(target_folder_path, folder)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    for root, dirs, files in os.walk(folder_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in folders_to_ignore]  # Игнорировать заданные папки при обходе
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.startswith('.') or os.path.isdir(file_path):
                continue
            normalized_name = normalize(file_name)
            file_extension = os.path.splitext(file_name)[1][1:].lower()
            try:
                if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
                    target = 'sensitive imager'
                elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
                    target = 'top-secret documents'
                elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
                    target = 'covert audio'
                elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
                    target = 'classified footage'
                elif file_extension in ['zip', 'gz', 'tar']:
                    archive_target_folder = os.path.join(target_folder_path, 'archived intel', normalized_name.replace('.' + file_extension, ''))
                    if not os.path.exists(archive_target_folder):
                        os.makedirs(archive_target_folder)
                    if os.path.exists(file_path):
                        try:
                            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                                zip_ref.extractall(archive_target_folder)
                            os.remove(file_path)
                            files_moved_count['archived intel'] += 1
                        except zipfile.BadZipFile:
                            logging.error(f"Ошибка: файл {file_path} поврежден и не может быть распакован.")
                            os.remove(file_path)
                        except Exception as e:
                            logging.error(f"Ошибка при обработке архива {file_path}: {e}")
                else:
                    target = 'miscellaneous classified data'
                
                if target:
                    shutil.move(file_path, os.path.join(target_folder_path, target, normalized_name))
                    files_moved_count[target] += 1
            except Exception as e:
                logging.error(f"Ошибка при перемещении файла {file_path} в '{target_folder_path}': {e}")

    logging.info(f"Файлы перемещены: {files_moved_count}")

    remove_empty_folders(folder_path)
    print("Secure Directory Organization Complete.")
    for category, count in files_moved_count.items():
        print(f"{count} files moved to {category}.")
