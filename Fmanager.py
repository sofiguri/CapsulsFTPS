import curses
import shutil
import os
from FSettings import folder_path as main_folder, log_path as log_path, User_path

us_name = ' '


def log(com, dat1=''):
    global us_name

    with open(log_path, 'a') as file:
        if com == 1:
            file.write(f'Пользователь {us_name} сделал следующее действие: Переименовал файл в {dat1}\n')
        elif com == 2:
            file.write(f'Пользователь {us_name} сделал следующее действие: Создал новый файл {dat1}\n')
        elif com == 3:
            file.write(f'Пользователь {us_name} сделал следующее действие: Создал новую папку {dat1}\n')
        elif com == 4:
            file.write(f'Пользователь {us_name} сделал следующее действие: Записал данные в файл {dat1}\n')
        elif com == 5:
            file.write(f'Пользователь {us_name} сделал следующее действие: Скопировал файл {dat1}\n')
        elif com == 6:
            file.write(f'Пользователь {us_name} сделал следующее действие: Удалил директорию {dat1}\n')
        elif com == 7:
            file.write(f'Пользователь {us_name} сделал следующее действие: Удалил файл {dat1}\n')


def list_files(stdscr, select_row):
    stdscr.clear()
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for i, file in enumerate(files):
        if i == select_row:
            stdscr.attron(curses.color_pair(1))
        else:
            stdscr.attroff(curses.color_pair(1))

        stdscr.addstr(i, 0, file)


def read_file(stdscr, content):
    stdscr.clear()
    stdscr.addstr(content)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('\n'):
            break
    stdscr.refresh()


def rename_file(stdscr, file):
    curses.cbreak()  

    stdscr.clear()
    stdscr.addstr(0, 0, "Введите новое имя для этого файла, затем нажмите Enter")
    stdscr.refresh()
    curses.echo()

    new_name = stdscr.getstr(1, 0).decode('utf-8')

    os.rename(file, new_name + ".txt")
    log(1, new_name)
    curses.nocbreak()


def add_file(stdscr, file):
    curses.cbreak()

    stdscr.clear()
    stdscr.addstr(0, 0, "Введите имя нового текстового файла, затем нажмите Enter")
    stdscr.refresh()
    curses.echo()

    name_file = stdscr.getstr(1, 0).decode('utf-8')

    file_path = os.path.join(file, name_file + ".txt")

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file_1:
            pass
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "Такой файл уже тут существует !!!")
        stdscr.refresh()
        curses.napms(3000)

    log(2, name_file)

    curses.nocbreak()


def add_dir(stdscr, file):
    curses.cbreak()

    stdscr.clear()
    stdscr.addstr(0, 0, "Введите имя новой папки, затем нажмите Enter")
    stdscr.refresh()
    curses.echo()

    name_dir = stdscr.getstr(1, 0).decode('utf-8')
    dir_path = os.path.join(file, name_dir)

    if not os.path.isfile(dir_path):
        os.mkdir(name_dir)
        log(3, name_dir)
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "Такая папка уже тут существует !!!")
        stdscr.refresh()
        curses.napms(3000)


def add_in_file(stdscr, file):
    curses.cbreak()

    stdscr.clear()
    stdscr.addstr(0, 0, "Введите текст, который хотите записать в файл, затем нажмите Enter")
    stdscr.refresh()
    curses.echo()

    file_text = stdscr.getstr(1, 0).decode('utf-8')

    with open(file, 'w') as file1:
        file1.write(file_text)
    log(4, file)


def copy_move_file(stdscr, file, params):
    stdscr.clear()
    stdscr.addstr(0, 0, "Выберите место для копирования/перемещения файла, затем нажмите Enter")
    stdscr.refresh()
    curses.echo()

    folder_path = stdscr.getstr(1, 0).decode('utf-8')

    folder_path_ab = os.path.abspath(folder_path)
    main_folder_ab = os.path.abspath(main_folder)

    folder_path_step = folder_path_ab.split(os.sep)
    main_folder_step = main_folder_ab.split(os.sep)

    if os.path.exists(folder_path) and (not os.path.isfile(folder_path)):
        if all(folder_path_step[i] == main_folder_step[i] for i in range(len(main_folder_step))):
            if params == 1:
                shutil.move(file, folder_path)
            else:
                shutil.copy(file, folder_path)
        else:
            stdscr.clear()
            stdscr.addstr(0, 0, "Нельзя выходить за пределы корневой папки")
            stdscr.refresh()
            curses.napms(3000)
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "Сюда невозможно вставить/переместить файл")
        stdscr.refresh()
        curses.napms(3000)
    log(5, file)


def main(stdscr):
    global us_name

    os.chdir(main_folder)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.curs_set(0)
    stdscr.nodelay(1)
    current_row_idx = 0

    with open(User_path, 'r') as filea:
        user_name = filea.read().strip()

    us_name = str(user_name)

    while True:
        try:
            bloak_read = False
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(os.listdir()):
                current_row_idx += 1
            elif key == ord('\n'):
                file = os.listdir()[current_row_idx]
                if os.path.isdir(file):
                    current_row_index = 0
                    os.chdir(file)
                else:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        read_file(stdscr, content)
                        bloak_read = True
            elif key == ord('q'):
                if os.getcwd() != main_folder:
                    parent_dir = os.path.dirname(os.getcwd())
                    os.chdir(parent_dir)
                    current_row_index = 0
            elif key == ord('r'):
                file = os.listdir()[current_row_idx]
                if not os.path.isdir(file):
                    bloak_read = True
                    rename_file(stdscr, file)

            elif key == ord('-'):
                file = os.listdir()[current_row_idx]
                if os.path.isdir(file):
                    log(6, file)
                    os.rmdir(file)
                else:
                    os.remove(file)
                    log(7, file)
            elif key == ord('+'):
                file = os.getcwd()
                add_file(stdscr, file)

            elif key == ord('='):
                file = os.getcwd()
                add_dir(stdscr, file)
            elif key == ord('a'):
                file = os.listdir()[current_row_idx]
                if not os.path.isdir(file):
                    bloak_read = True
                    add_in_file(stdscr, file)
            elif key == ord('c') or key == ord('m'):
                file = os.listdir()[current_row_idx]
                if not os.path.isdir(file):
                    bloak_read = True
                    if key == ord('c'):
                        copy_move_file(stdscr, file, 0)
                    else:
                        copy_move_file(stdscr, file, 1)
            elif key == 27:
                break

            if bloak_read == False:
                list_files(stdscr, current_row_idx)
        except:
            pass


curses.wrapper(main)
