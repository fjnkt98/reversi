from setuptools import setup

setup(
    name="reversi",
    version="0.1.0",
    install_requires=[],
    extras_require={"develop": ["mypy", "flake8", "black"]},
    entry_points={"console_scripts": {"app = reversi.reversi:main"}},
)
