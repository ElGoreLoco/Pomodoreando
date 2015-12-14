from setuptools import setup

import pomodoreando

setup(
    name="Pomodoreando",
    version=pomodoreando.__version__,
    author="ElGoreLoco",
    author_email="esegoreloco@gmail.com",
    url="https://github.com/ElGoreLoco/Pomodoreando",
    description="Aplicación para manejar tus pomodoros",
    long_description=open("README.md").read(),
    license="MIT",
    packages=["pomodoreando"],
    entry_points={"console_scripts":
                  ["pomodoreando=pomodoreando.pomodoreando:main"]},
    install_requires="docopt")
