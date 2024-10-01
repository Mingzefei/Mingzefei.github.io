---
title: "Scientific Project Organization"
description: ""
date: 2024-10-01T21:10:13+08:00
tags: 
  - "academic"
  - "code"
sidebar: true
---

A complete scientific project involves multiple aspects, including data, code, and paper reports. Organizing these elements effectively contributes to project management, reproducibility, backups, and traceability.

Based on practical experience, here is a project organization method inspired by the work of [Mario Krapp/semic-project](https://gitlab.pik-potsdam.de/krapp/semic-project) and [Joshua Cook](https://joshuacook.netlify.app/posts/2024-07-27_python-data-analysis-org/).

This method is suitable for the following types of projects:
- Core code written mainly in Python;
- Paper reports primarily written in LaTeX and Markdown;
- Version control using Git.

Additionally, this article suggests using the following tools:
- `uv`: to install dependencies;
- `cookiecutter`: to generate project structures;
- `Sphinx`: to automatically generate API documentation.

While these tools are not mandatory, you can replace them with alternatives based on your preferences. This article will demonstrate how to create and organize projects using these tools.

## Setting Up the Project Structure

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) is a command-line tool used to quickly generate project structures from predefined templates.

### Quick Start

First, install the tool with the following command:

```shell
uv pip install cookiecutter
```

Next, use this tool to install the project structure template provided by [Mingzefei/cookiecutter-science](https://github.com/Mingzefei/cookiecutter-science):

```bash
cookiecutter https://github.com/Mingzefei/cookiecutter-science.git
```

Note: You can find other project templates at [special templates](https://github.com/cookiecutter/cookiecutter#special-templates).

Follow the prompts to fill in the required information, and the project structure will be generated at the current location.

### Project Structure

```text
.
├── AUTHORS.md                      <- Information about project authors
├── LICENSE                         <- Open source license for the project
├── README.md                       <- Project documentation, including description and installation instructions
├── backup                          <- Backup folder for configurations, results, etc., not tracked by version control
├── config                          <- Configuration files directory
│   └── config.yaml                 <- Configuration file with calculation parameters and settings
├── data                            <- Project data, not tracked by version control
│   ├── external                    <- External datasets from other research teams for validation or comparison
│   ├── interim                     <- Intermediate data, processed for exploration and further steps
│   ├── processed                   <- Final processed datasets for modeling and analysis
│   └── raw                         <- Raw, unprocessed data
├── docs                            <- Documentation and research literature related to the project
├── notebooks                       <- Jupyter Notebook files for initial exploration, code experiments, and demonstrations
│   └── 00_draft_example.ipynb       <- Example Notebook as a draft
├── pyproject.toml                  <- Project configuration file for dependencies and packaging
├── reports                         <- Academic reports and project reports
│   ├── Makefile                    <- Makefile for compiling LaTeX reports
│   ├── archive                     <- Archived drafts
│   ├── figures                     <- Figures and charts used in reports
│   ├── main.tex                    <- Main LaTeX source file for the report
│   └── si.tex                      <- Supplemental information or materials in LaTeX
├── results                         <- Storage location for experimental or analysis results, not tracked by version control
├── scripts                         <- Executable scripts for data download, cleaning, backups, etc.
│   ├── __init__.py                 <- Initialization file for script modules
│   ├── backup.py                   <- Data backup script
│   ├── clean.py                    <- Data cleaning script
│   ├── config_loader.py            <- Configuration file loader
│   ├── data_downloader.py          <- Data download script
│   └── paths.py                    <- Project paths configuration script, defining folder paths
└── {{cookiecutter.project_slug}}    <- Core project code (referred to as `src`), which can be packaged as a Python package
    ├── __init__.py                 <- Project package initialization file
    ├── cli.py                      <- Command-line interface for core project functionalities
    ├── data                        <- Data processing logic functions
    │   ├── __init__.py             
    │   └── clean_data.py           <- Data cleaning implementation logic
    ├── external                    <- External libraries or code, not tracked by version control
    ├── models                      <- Code for model building and training
    │   └── __init__.py             
    ├── plot                        <- Data visualization logic
    │   ├── __init__.py             
    │   └── plot_style.py           <- Script for defining data visualization styles and themes
    └── utils                       <- Utility functions, including file I/O, logging, etc.
        ├── __init__.py             
        ├── file_io.py              <- File input/output logic
        └── logger.py               <- Logging logic
```

### Explanation

(The `{{cookiecutter.project_slug}}` is referred to as `src` below.)

1. `src` is the core code where input/output are abstract data structures and do not involve specific files or paths. It can be packaged as a standalone Python package.
    - `src/data`: Data processing logic functions.
    - `src/utils`: Utility functions like file I/O and logging.
    - `src/models`: Logic for model construction.
    - `src/plot`: Logic for data visualization.
2. `scripts` contains executable scripts for tasks like data downloading, model training, and results backup. These scripts can call `scripts/paths.py`, `scripts/config_loader.py`, and `src` to retrieve paths, configurations, and logic.
    - `scripts/paths.py`: Defines project folder paths for inputs and outputs, usually fixed.
    - `scripts/config_loader.py`: Configuration loader for the project, specifying experimental parameters, modifiable as needed.
3. `notebooks` holds all Jupyter Notebook files, initially for quick code prototyping and exploration, later for execution and presentation.
    - Regularly refactor the code in `notebooks` into `src` and `scripts` to maintain clean notebook files and enable project automation.
    - Jupyter Notebook filenames should follow the format `<incrementing_number>_<descriptive_name>.ipynb`, e.g., `01_data_process.ipynb`. Use two-digit numbers `xy`, where `x` has the following meanings:
        - 0: Draft
        - 1: Data
        - 2: Models
        - 3: Results (e.g., visualizations)
        - 4: Reports
4. `docs` contains project-related literature and technical documentation.
5. `reports` stores final academic reports (e.g., LaTeX files) and archived drafts (e.g., md, docx, pptx, pdf, etc.).
6. `data` holds project data files, usually large and not managed by version control.
    - `data/raw`: Original data from the source, unmodified.
    - `data/interim`: Intermediate data, cleaned and processed for further steps.
    - `data/processed`: Final data for modeling and analysis.
    - `data/external`: External datasets from other research teams for validation and comparison.

## Version Control

Use `git` for version control and upload the project to `GitHub` for team collaboration and backup.

You can find more information about `git` and `GitHub` from their respective documentation.

## Virtual Environment Management

You can use `conda` to create a virtual environment, but I recommend creating a virtual environment within the project folder to avoid `conda` name conflicts.

```bash
uv venv # Create a virtual environment
source .venv/bin/activate # Activate the virtual environment
```

You can install dependencies with the following command:

```shell
uv pip install <library> # Install dependencies
```

## Core Code Development

Develop logic functions and classes within `src`, ensuring that inputs and outputs are abstract data structures without specific files or paths involved. 
`src` can be installed as a package in the local virtual environment.

### Completing the Project Configuration File

The `pyproject.toml` file is used to configure and manage the project. Modify the contents as needed.

Here is a simple example:

```toml
# Build system configuration
[build-system]
requires = [
    "setuptools", 
    "setuptools_scm[toml]",
    "wheel"]
build-backend = "setuptools.build_meta"

# Project metadata
[project]
name = "my_project"  # Project name
description = "project description"  # Project description
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dynamic = ["version"]
requires-python = ">=3.8"  # Minimum Python version
dependencies = [
    "numpy",  # Project dependencies, not exhaustive
    "pandas",
    "jupyterlab",
    "matplotlib"
]
classifiers = ["Private :: Do Not Upload"] # If it's a private project, avoid uploading to PYPI

# Optional development tools
[project.optional-dependencies]
dev = [
    "ruff",   # Code linter
    "pytest"  # Unit testing tool
]

[tool.setuptools]
packages = ["src"] # Path to the project code (src)

[tool.setuptools_scm] # Use GitHub tags as the version

 number
version_scheme = "post-release"
local_scheme = "no-local-version"
```

A more complete version would look like this:

```toml
# Build system configuration
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

# Project metadata
[project]
name = "<example_project>"
version = "<0.1.0>"
description = "<An example Python project.>"
readme = "README.md"  # README file for the project
license = {file = "LICENSE"}
authors = [
    {name = "<name>", email = "<e-mail>"}
]
maintainers = [
    {name = "<name>", email = "<e-mail>"}
]
keywords = ["example", "sample", "project"]
repository = "https://github.com/example/example_project"
documentation = "https://docs.example.com"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent"
]
dependencies = [
    "jupyterlab",
    "matplotlib",
    "numpy",
    "pandas"
]

# Optional dependencies configuration
[project.optional-dependencies]
dev = [
    "ruff",
    "pytest>=6.0",
    "black",
    "flake8",
    "mypy"
]
docs = [
    "sphinx",
    "sphinx-rtd-theme"
]

# Plugin and tool configurations
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310']

[tool.flake8]
max-line-length = 88
exclude = ["tests/*", "build/*"]

[tool.mypy]
strict = true

[tool.setuptools]
packages = ["src"] # Path to the project code (src)

[tool.setuptools_scm] # Use GitHub tags as the version number
version_scheme = "post-release"
local_scheme = "no-local-version"
```

### Install Core Code Locally

```shell
uv pip install -e .
```

Alternatively, use the development dependencies:

```shell
pip install -e .[dev]
```

NOTE: The `-e` or `--editable` flag installs the package in editable mode, meaning changes to the `src` code will take effect immediately without needing reinstallation.

For example, you can directly import it in `ipython` or scripts:

```python
import my_project
```

### Update the Project Configuration File

During the project, new dependencies may be added or removed, requiring updates to the dependencies section in the project configuration file.  
Use `pipreqs` to automatically generate a specific list of dependencies and manually update `pyproject.toml` accordingly.

```shell
uv pip install pipreqs
pipreqs <project_path>
```

### Create Command-Line Mode (Optional)

Use `Typer` to create a command-line interface (CLI) for easier usage.

Create a `cli.py` file in the project package and write the CLI code:

```python
import typer

app = typer.Typer()

@app.command()
def hello_world(
    name: str = typer.Option(..., help="Your name"),  # Required parameter
    shout: bool = typer.Option(False, help="Whether to shout")  # Optional boolean parameter
) -> None:
    """
    Greet the user.
    """
    greeting = f"Hello, {name}!"
    if shout:
        greeting = greeting.upper() 
    print(greeting) 

@app.command()
def goodbye_world(
    reason: str = typer.Option(None, help="Reason for leaving"),  # Optional parameter
    formal: bool = typer.Option(True, help="Use formal goodbye")  # Optional boolean parameter
) -> None:
    """
    Say goodbye to the user.
    """
    if formal:
        message = f"Goodbye! Reason: {reason or 'No reason provided.'}" 
    else:
        message = "Bye!" 
    print(message) 

if __name__ == "__main__":
    app()
```

Add the command-line entry point to `pyproject.toml`:

```toml
[project.scripts]
"proj" = "my_project:cli.app"
```

Then use it from the command line:

```shell
proj --help
proj hello-world --name Alice --shout
proj goodbye-world --resason "I have to go"
```

NOTE: `Typer` automatically converts underscores (`_`) in option names to hyphens (`-`).

### Code Linting

Use `ruff`, `black`, `flake8`, and `mypy` to enforce code quality and consistency.

## Project Release

### Metadata

Make the following modifications in `pyproject.toml`:

```toml
classifiers = [ 
	"Development Status :: 4 - Beta", 
	"Programming Language :: Python :: 3", 
	"License :: OSI Approved :: MIT License", 
	"Operating System :: OS Independent", 
]
```

- `Development Status :: 4 - Beta`: Indicates that the project is in the Beta phase, where it's mostly functional but may have significant improvements or bugs.
- `Programming Language :: Python :: 3`: Specifies that the project is written in Python 3.
- `License :: OSI Approved :: MIT License`: Indicates that the project is open source under the MIT license.
- `Operating System :: OS Independent`: Means the project can run on any operating system.

### Generate Release Files

```shell
python -m build
```

### Upload to PyPI

```shell
twine upload dist/*
```

NOTE: You can automate releases using GitHub Actions.

## Project Documentation

Use `Sphinx` to automatically generate API documentation for the Python project, ensuring code is well-documented.

### Using Sphinx

```bash
# 0. Install
pip install sphinx
# 1. Initialize
cd docs
sphinx-quickstart
# 2. Configure
vi source/conf.py
# --- Enter editing mode
# 1) Add path
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))
# 2) Add extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
]
# 3) Set theme
html_theme = 'sphinx_rtd_theme'
# --- Exit editing mode
# 3. Compile
sphinx-apidoc -o source ../src/
make html
```

## Future Features

- Code tests
- Code formatting checks
- Continuous integration

## References

- Some principles for writing code: [Guiding Design Principles](https://nsls-ii.github.io/scientific-python-cookiecutter/guiding-design-principles.html#write-for-readability) (Many design ideas in this project were inspired by this)
- Some useful cookiecutter templates:
    - [NSLS-II/scientific-python-cookiecutter](https://github.com/NSLS-II/scientific-python-cookiecutter)
    - [jbusecke/cookiecutter-science-project](https://github.com/jbusecke/cookiecutter-science-project/tree/master)
