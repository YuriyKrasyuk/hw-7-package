from setuptools import setup, find_namespace_packages


setup(
    name='clean_folder',
    version='1.0.0',
    description='Script for the sorting files in folder',
    author='Yuriy Krasyuk',
    author_email='ykrasyuk@gmail.com',
    url='https://github.com/YuriyKrasyuk/hw-6-sort-folder',
    license = 'MIT',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.sort_files:main'],
    }
)