from setuptools import setup

setup(
    name='tickets',
    version='1.2',
    py_modules=['tickets','stations'],
    install_requires=['requests','docopt','prettytable'],
    #当执行tickets命令时,调用tickets中的cli方法
    entry_points={
        'console_scripts': ['tickets=tickets:cli']
    }
)