import setuptools, shutil, os, sys
from nachomines import __version__
from nachomines.scripts.utils import fix_path

if "install" in sys.argv and sys.platform == "linux":
    if os.path.exists("/usr/share/applications"):
        shutil.copy(
            "nachomines/nachomines.desktop",
            "/usr/share/applications/nachomines.desktop",
        )
    if os.path.exists("/usr/share/icons"):
        shutil.copy("nachomines/icon.png", "/usr/share/icons/nachomines.png")

setuptools.setup(
    version=__version__,
    package_data={"nachomines" : ["*.png", fix_path("resources/images/bitmap/*"), fix_path("resources/sounds/*")]},
    python_requires=">=3.6",
)
