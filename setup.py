from setuptools import setup, find_packages
import re

with open("README.md", "r") as f:
    long_description = f.read()

with open('src/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1) or ''

if not version:
    raise RuntimeError('No Version Found.')


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    line_iter = (line.strip() for line in open(filename))
    return [line for line in line_iter if line and not line.startswith("#")]


setup(
    name='IreneAPIWrapper',
    version=version,
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    url='https://github.com/MujyKun/IreneAPIWrapper',
    license='MIT License',
    author='MujyKun',
    author_email='mujy@irenebot.com',
    description="A wrapper for Irene's API and connects with a websocket connection.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',

)
