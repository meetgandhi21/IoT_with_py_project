from setuptools import setup, find_packages

setup(
    name='rpi_ha_server',
    version='0.1.0',
    description='RPI based Home Automation Server which controlls room light based on number of people present in room',
    author='Meet Gandhi',
    author_email='g.meet2194@gmail.com',
    
    python_requires='>=3.5',
    packages=find_packages(),
    scripts=['bin/rpi_ha_server'],
    #add any required third party module in below list
    install_requires=[
            "AWSIoTPythonSDK"]
)

