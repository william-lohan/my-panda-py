from setuptools import setup

setup(
    name='mypanda',
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'gui_apps': {
                'main': 'main.py',
                'mypanda': 'filename.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': '$USER_APPDATA/Asteroids/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',

                # Path to a specific file
                'CREDITS.txt',

                # All files in the assets/textures/ directory, but not in subdirectories
                # (use ** instead of * if that is desirable)
                'assets/textures/*',

                # All files with the .jpg extension in any subdirectory under assets/,
                # even if nested under multiple directories
                'assets/**/*.jpg',

                # A file with the .egg extension anywhere in the hierarchy
                '**/*.egg',
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],

            'platforms': ['manylinux2014_x86_64', 'macosx_10_9_x86_64', 'win_amd64'],
        }
    }
)
