from datetime import datetime
import os



def get_file_path(extension, prefix=None, dir_path=None):
    cur_time = datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    file_name = f'{cur_time}.{extension}'
    file_name = f'{prefix}_{file_name}' if prefix is not None else file_name
    file_path = os.path.join(dir_path, file_name) if dir_path is not None else file_name
    return file_path