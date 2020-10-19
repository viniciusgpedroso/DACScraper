import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="DACScraper",
    version="1.0.0",
    description="Scraper for some of DAC (https://www.dac.unicamp.br/) public data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/viniciusgpedroso/DACScraper",
    packages=["reader"],
    include_package_data=True,
    install_requires=["scrapy", "mysql-connector-python"],
)
