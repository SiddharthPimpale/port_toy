from setuptools import setup, find_packages

setup(
    name="porttoy",
    version="1.0.0",
    description="A utility tool for scanning and managing ports and processes.",
    author="Siddharth Pimpale",
    author_email="siddharthpimpale10@gmail.com",
    packages=find_packages(),  # Finds all packages (subfolders with __init__.py)
    install_requires=[
        'psutil>=5.9.0',
        'colorama>=0.4.4',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'porttoy=porttoy.main:main',  # CLI command = module path
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
)
