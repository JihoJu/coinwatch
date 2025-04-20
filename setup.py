from setuptools import setup, find_packages

setup(
    name="coinwatch",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.1",
        "websockets==12.0",
        "aiokafka==0.10.0",
        "orjson==3.10.6",
        "asyncio==3.4.3",
        "pytest==8.3.5",
        "pytest-asyncio==0.26.0"
    ],
)