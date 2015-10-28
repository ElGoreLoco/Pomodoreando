from setuptools import setup

__version__ = "0.1.0"

setup(name="Pomodoreando",
      version=__version__,
      author="ElGoreLoco",
      author_email="esegoreloco@gmail.com",
      url="https://github.com/ElGoreLoco/Pomodoreando",
      description="Aplicación para manejar tus pomodoros",
      long_description="Pomodoreando es un programa pensado para manejar tus \
pomodoros de una manera rápida y sencilla. Además de su función de control de\
 pomodoros, puedes utilizarlo como un cronómetro normal.",
      license="MIT",
      packages=["pomodoreando"],
      scripts=["scripts/pomodoreando"],
      install_requires="docopt")
