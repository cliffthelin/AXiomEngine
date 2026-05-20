from setuptools import setup, find_packages

setup(
    name="axiomengine-governance",
    version="1.5.0",
    description="AXiomEngine Governance Infrastructure (Additive Layer)",
    author="AXiomEngine Maintainers",
    # find_packages will now find 'scripts' because of __init__.py
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24",
        "pydantic>=2",
        "jsonschema>=4",
        "psutil>=5",
    ],
    entry_points={
        "console_scripts": [
            "gov = scripts.governance_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
