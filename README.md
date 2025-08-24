# Python Learning

Python learning, tools, and reusable snippets for automating various tasks.

## Environment Setup

### Install PDM

The dependency manager used in this project is [pdm](https://github.com/pdm-project/pdm). To install it, run the following command:

```bash
$ curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

Or, alternatively, other [installation methods](https://pdm-project.org/en/latest/#installation) can be used.

### Install Dependencies

The specified python version in `pyproject.toml` is `>=3.11`, and so a **python 3.11** interpreter should be used. 

#### Conda

To do so with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):

```bash
$ conda search python | grep " 3\.\(10\|11\|12\)\."
$ yes | conda create --name python_learning python=3.11.9
$ conda activate python_learning
$ pdm use -f $(which python3)
$ pdm install
```

#### Virtualenv

To do so with [virtualenv](https://github.com/pypa/virtualenv), use the [pdm venv](https://pdm-project.org/en/latest/reference/cli/#venv) command:

```bash 
$ pyenv install --list | grep " 3\.\(10\|11\|12\)\."
$ pyenv install 3.11.9
$ pdm venv create --name python_learning --with virtualenv 3.11.9 
# To activate the virtual environment
$ eval $(pdm venv activate python_learning) 
$ pdm install
```

Use `--with venv` to create the virtual environment using `venv` (comes with standard library) instead of `virtualenv` (third-party package but more performant). To create the venv in the project root instead of `pdm config venv.location`, omit the `--name` option:

```bash
$ pdm config venv.in_project true
$ pdm venv create --with venv 3.11.9
```
