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
    package_data={"nachomines" : ["*.png", fixPath("resources/images/bitmap/*"), fixPath("resources/sounds/*")]},
    python_requires=">=3.6",
)
