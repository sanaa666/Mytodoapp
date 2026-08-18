from configparser import ConfigParser
from pathlib import Path

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / filename
    parser.read(file_path)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {file_path} file')

    return db

if __name__ == '__main__':
    config = load_config()
    print(config)