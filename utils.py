import os

def organize_type(cwd, downloads_dir, element):
    type = element['type']
    extentions = element['extensions']

    print(f"Organizing {type}")
    
    # for element in extentions:
    #     extention = element[0]

    type_dir = os.path.join(downloads_dir, type)

    if os.path.exists(type_dir):
        print(f'"{type_dir}" exists!')
    else:
        print(f'"{type_dir}" does not exist. Lets try to make it.')
        try:
            os.mkdir(type_dir)
            print(f"{type} directory created successfuly!")
        except OSError as error:
            print(error)

    for dir in os.listdir():
        if os.path.isfile(dir):
            for element in extentions:
                ext = element[0]
                if ext in dir:
                    src_path = os.path.join(cwd, dir)
                    dst_path = os.path.join(type_dir, dir)
                    os.rename(src_path, dst_path)
