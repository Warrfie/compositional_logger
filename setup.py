from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="compositional_logger",
    version="0.1.0",
    description="Package for data logging in compositional style",
    long_description=long_description,
    url="https://github.com/Warrfie/compositional_logger",
    author="Kuklikov Maxim (Warrfie)",
    author_email="warrfie@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="QA, logging, combidata, testing API, testing, autotesting",
    packages=find_packages(),
    python_requires=">=3.10, <4",
    project_urls={
        "Telegram": "https://t.me/sasisochka",
        "Main page": "https://github.com/Warrfie/compositional_logger"
    },
)

