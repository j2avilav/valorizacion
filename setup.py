from setuptools import find_packages, setup

# Read the contents of requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="valorizacion_ts",
    version="0.1",
    description="Estudios de valorización de las instalaciones de los sistemas de tranmisión para el periodo 2024-2027",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="B9 Ingeniería SpA",
    author_email="contacto@b9.cl",
    url="https://github.com/b9ingenieria/valorizacionTx",
    packages=find_packages(where="."),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "valorizacion-run-workflow=scripts.workflow:main",
        ],
    },
)
