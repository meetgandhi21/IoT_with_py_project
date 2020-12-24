from setuptools import setup, find_packages

setup(
    name='event_sensor',
    version='0.1.0',
    description='Generates an input event for rpi_ha_server',
    author='Meet Gandhi',
    author_email='g.meet2194@gmail.com',
    
    python_requires='>=3.5',
    packages=find_packages(),
    scripts=['bin/event_sensor'],
    #add any required third party module in below list
    install_requires=[]
)

