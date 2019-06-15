from setuptools import setup, find_packages

setup(
    name="recreation_checker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
            'twilio',
            'requests',
            'python-dotenv'
        ],
)