from setuptools import setup, find_namespace_packages

setup(
    name='agent_book',
    version='0.0.5',
    entry_points={
        'console_scripts': []
    },
    description='Agent Address book',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/peakodev/team007/tree/main/agent_book',
    author='Team007',
    author_email='peakodev@gmail.com',
    packages=find_namespace_packages(),
    install_requires=[],
)