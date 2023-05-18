import os
from pathlib import Path
from configparser import RawConfigParser

SYSTEM_APPS_DIR = Path("/").joinpath("usr", "share", "applications");
USER_APPS_DIR = Path.home().joinpath(".local", "share", "applications");
ICONS_DIR = Path("/").joinpath("usr", "share", "icons");

def read_desktop_files(directory) -> list[str]:
    desktop_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".desktop"):
                desktop_files.append(os.path.join(root, file))
    return desktop_files

def filter_by_category(files: list[str], category: str) -> list[dict]:
    filtered_files = []
    for file in files:
        parser = RawConfigParser()
        parser.read(file)
        if parser.has_option('Desktop Entry', 'Categories'):
            categories = parser.get('Desktop Entry', 'Categories').split(';')
            if category in categories:
                Name = parser.get('Desktop Entry', 'Name')
                Comment = parser.get('Desktop Entry', 'Comment')
                Exec = parser.get('Desktop Entry', 'Exec')
                Icon = parser.get('Desktop Entry', 'Icon')
                Icon = str(ICONS_DIR.joinpath(Icon))
                filtered_files.append({ 'Name': Name, 'Comment': Comment, 'Exec': Exec, 'Icon': Icon })
    return filtered_files

def get_game_apps() -> list[dict]:
    # Specify the category to filter by
    category = 'Game'

    # Read the .desktop files
    files = read_desktop_files(SYSTEM_APPS_DIR)
    files += read_desktop_files(USER_APPS_DIR)

    # Filter the files by category
    return filter_by_category(files, category)

if __name__ == "__main__":
    filtered_files = get_game_apps()
    # Print the filtered file paths
    for file in filtered_files:
        print(file)
