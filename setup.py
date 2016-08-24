import os
import setuptools

setuptools.setup(
    name="mattermost-integration-pivotaltracker",
    version="0.1",
    url="https://git.studioqi.ca/lefebvre/mattermost-integration-pivotaltracker",

    author="Pierre Paul Lefebvre",
    author_email="info@pierre-paul.com",

    description="GitLab Integration Service for PivotalTracker",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),

    packages=setuptools.find_packages(),

    install_requires=[
        "Flask==0.10.1",
        "requests==2.8.1",
        "six",
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    entry_points={
        'console_scripts': [
            'mattermost_pivotaltracker = mattermost_pivotaltracker.server:main',
        ]
    }
)
