import setuptools, shutil, os, sys
from nachomines import __version__
from nachomines.scripts.fixPath import fixPath

if sys.platform == "linux":
    if os.path.exists("/usr/share/applications"):
        shutil.copy(
            "nachomines/nachomines.desktop",
            "/usr/share/applications/nachomines.desktop",
        )
    if os.path.exists("/usr/share/icons"):
        shutil.copy("nachomines/icon.png", "/usr/share/icons/nachomines.png")

setuptools.setup(
    version=__version__,
<<<<<<< HEAD
    author="NachoMonkey",
    description="Simple python minesweeper game using pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nachomonkey/NachoMines",
    packages=["nachomines", "nachomines.scripts"],
    package_data={"nachomines" : ["*.png", fixPath("resources/images/bitmap/*"), fixPath("resources/sounds/*")]},
    install_requires=["setuptools", "pygame"],
    zip_safe=False,
=======
    package_data={"nachomines": ["*.png", fixPath("resources/images/bitmap/*")]},
>>>>>>> 353db45af5fa5625a3ba8535c8b848581fec8f1f
    python_requires=">=3.6",
)
