import setuptools, shutil, os
from nachomines import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.path.exists("/usr/share/applications"):
    shutil.copy("nachomines/nachomines.desktop", "/usr/share/applications/nachomines.desktop")
if os.path.exists("/usr/share/icons"):
    shutil.copy("nachomines/icon.png", "/usr/share/icons/nachomines.png")

setuptools.setup(
    name="nachomines",
    version=__version__,
    author="NachoMonkey",
    description="Simple python minesweeper game using pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nachomonkey/NachoMines",
    packages=["nachomines", "nachomines.scripts"],
    package_data={"nachomines" : ["*.png", "resources/images/bitmap/*"]},
    install_requires=["setuptools", "pygame"],
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "nachomines = nachomines.scripts.main:run",
            ]
        },
)
