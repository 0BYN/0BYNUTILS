from setuptools import setup, find_packages

setup(
    name="obynutils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "disnake",
        "redis",
        "SQLAlchemy",
        "asyncpg",
        "quart",
        "quart-cors",
    ],
    description="A set of utility functions for Obyn bots",
    author="GizmoShiba",
    author_email="gizmoshiba@gmail.com",
    url="https://github.com/gizmoshiba/obyn-utils",
    classifiers=[],
    python_requires=">=3.8",
)
