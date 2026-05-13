from setuptools import setup, find_packages

setup(
    name="axiomengine-governance",
    version="1.5.0",
    description="AXiomEngine Governance Infrastructure (Additive Layer)",
    author="AXiomEngine Maintainers",
    # find_packages will now find 'scripts' because of __init__.py
    packages=find_packages(),
    install_requires=[
        # Core is stdlib-first
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
