import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easynmpython",
    version="1.0.14",
    author="Adam Raźniewski",
    author_email="adam@razniewski.eu",
    description="Easy NetworkManager DBUS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Razikus/easynmpython",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    # It requires DBUS python3-dbus python-dbus
    install_requires=[
    ]
)