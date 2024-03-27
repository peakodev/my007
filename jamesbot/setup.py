from setuptools import setup, find_namespace_packages

setup(
    name='jamesbot',
    version='0.0.1',
    entry_points={
        'console_scripts': ['james = jamesbot.jamesbot:bot_start']
    },
    description='jamesbot',
    author='Team007',
    author_email='peakodev@gmail.com',
    packages=find_namespace_packages(),
    install_requires=[
        'agent_notes>=0.0.1',
        'agent_book>=0.0.5',
        'xfiles_sorter>=0.0.1',
        'faker',
        'prompt_toolkit',
        'colorama'
    ],
)