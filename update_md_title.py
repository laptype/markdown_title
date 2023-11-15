import glob
import os

def get_file_name(file_path):
    file_name = file_path.split('\\')[-1]
    file_dir = file_path.split('\\')[-2]
    return file_name.split('.')[0], file_dir


def get_date(row, i):
    if row.startswith('date: ') and i < 5:
        _, date, *_ = row.split(' ')
        y, m, d = date.split('-')
        return (y, m, d)
    else:
        return None

def update_one_file(file_path, menu, menu_start, menu_end):
    data = []
    append_menu = False
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, row in enumerate(f.readlines()):
            if i < menu_start:
                data.append(row)
            elif i > menu_start and i < menu_end:
                if not append_menu:
                    for m in menu:
                        data.append(m)
                    append_menu = True
            else:
                data.append(row)
    with open(file_path, 'w', encoding='utf-8') as f:
        for row in data:
            f.write(row)

def get_menu(file_path, menu=None):

    file_name, file_dir = get_file_name(file_path)
    menu_single = []
    if menu is None:
        menu = []
    date = None
    title = None

    menu_start = -1
    menu_end = -1

    with open(file_path, 'r', encoding='utf-8') as f:
        for i, row in enumerate(f.readlines()):
            row = row.strip(' \t\n')
            if date is None:
                date = get_date(row, i)
            if date is None:
                continue

            if row.startswith('---'):
                if menu_start == -1:
                    menu_start = i+1
                elif menu_end == -1:
                    menu_end = i-1
                else:
                    continue

            if not row.startswith('#'):
                continue

            head = row.split(' ')[0]

            str_t = '  '*(len(head)-1)
            str_title = row[len(head):].strip(' \t\n')
            y, m, d = date
            str_link = f"/{y}/{m}/{d}/{file_dir}/{file_name}/#{str_title}"
            if title is None:
                title = f"# [{str_title}]({str_link})\n\n"
                menu.append(title)
                menu_single.append(f"# {str_title}\n")
            elif menu_end != -1:
                menu.append(f"{str_t}- [{str_title}]({str_link})\n")
                menu_single.append(f"{str_t}- [{str_title}](#{str_title})\n")

    menu.append('\n')
    menu_single.append('\n')

    update_one_file(file_path,menu_single, menu_start, menu_end)

    return menu


def write_md(menu, targetname="res.md"):
    with open(targetname, 'w+', encoding='utf-8') as f2:
        for m in menu:
            f2.write(m)

def get_file_path_list(file_root):
    md_files = glob.glob(os.path.join(file_root, '*.md'))
    return md_files

if __name__ == '__main__':
    menu = []

    md_path_list = get_file_path_list('D:\lanbo\github\laptype_github_code\source\_posts\Leetcode')
    for path in md_path_list:

        menu = get_menu(path, menu=menu)


    write_md(menu)
#