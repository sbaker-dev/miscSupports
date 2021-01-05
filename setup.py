# Copyright (C) 2020 Samuel Baker

DESCRIPTION = "Supporting common methods for multiple packages and repositories I have written"
LONG_DESCRIPTION = """

Source code can be found at the following [git repo][repo]


[repo]: https://github.com/sbaker-dev/miscSupports
"""

LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

DISTNAME = 'miscSupports'
MAINTAINER = 'Samuel Baker'
MAINTAINER_EMAIL = 'samuelbaker.researcher@gmail.com'
LICENSE = 'MIT'
DOWNLOAD_URL = "https://github.com/sbaker-dev/miscSupports"
VERSION = "0.02.1"
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'scipy',
    'numpy',
    'PyYAML']

CLASSIFIERS = [
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
]

if __name__ == "__main__":

    from setuptools import setup, find_packages

    import sys

    if sys.version_info[:2] < (3, 7):
        raise RuntimeError("miscSupports requires python >= 3.7.")

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        license=LICENSE,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(),
        classifiers=CLASSIFIERS
    )
