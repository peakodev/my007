import os
import shutil
import zipfile
from xfiles_sorter import organize_files, remove_empty_folders


def handle_command(command):
    if command == "decipher":
        # Здесь вы можете запросить у пользователя путь к папке или задать его заранее
        folder_path = input("Введите путь к папке для расшифровфки: ")
        target_folder_path = input("Введите путь куда переместить расшифрованные файлы:")
        organize_files(folder_path, target_folder_path)
    elif command == "remove":
        folder_path = input("Введите путь к папке для удаления файлов: ")
        remove_empty_folders(folder_path)
    # elif command == "normalize":
    #     folder_path = input("Введите путь к папке для розшифроки: ")
    #     normalize_files(folder_path)
    elif command == "help":
        print("Доступные команды:\ndecipher - расшифровать файлы в указанной папке\nremove - remove folder\nexit - выйти из программы") #\nnormalize - translate
    elif command == "exit":
        print("Выход из программы...")
        exit()
    else:
        print("Неизвестная команда. Введите 'help' для списка доступных команд.")

def main():
    print("Консольный бот для разшифровки файлов. Введите 'help' для списка команд.")
    while True:
        command = input("Введите команду: ")
        handle_command(command)

if __name__ == "__main__":
    main()
