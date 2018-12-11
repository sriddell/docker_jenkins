import setuptools

setuptools.setup(
    install_requires=[
        'requests>=2.18.2',
        'click>=6.7',
        'jinja2'
    ],
    name="docker_jenkins_utils",
    version="0.0.1",
    author="Shane Riddell",
    author_email="shaneridell@icloud.com",
    description="Package of utilities for dockerized jenkins",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)