from setuptools import setup, find_packages

setup(
    name='AutoCadence',
    version='1.0.0',
    description='Aplicativo com instalador usando Tkinter',
    author='Tudo-em-Nuvem',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        'gui_scripts': [
            'autocadence = app:App'
        ]
    },
)
