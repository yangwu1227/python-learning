## Saving environment variables

If we wish to store environment variables for a specific environment "env_name", say, sensitive credentials. We can write a shell script named `env_vars`. For Mac and Linux:

1. In the terminal, find the conda directory:

```console
$ conda activate <env_name>
$ echo $CONDA_PREFIX
```

2. By default, environments are installed into the `envs` directory in the conda directory. We need to create the following subdirectories and files within the directory of the environment for which we wish to store the environment variable:

```console
$ cd $CONDA_PREFIX

$ mkdir -p ./etc/conda/activate.d
$ mkdir -p ./etc/conda/deactivate.d

$ touch ./etc/conda/activate.d/env_vars.sh
$ touch ./etc/conda/deactivate.d/env_vars.sh
```
* The `mkdir -p` command creates the sub-directories under the current directory. It will create the parent directory first, if it doesn't exist. If it already exists, it will proceed to create the sub-directories. The `touch` command is used to create files without any content.

3. Open the shell scripts and edit using absolute or relative path from within `$CONDA_PREFIX`:

```console
$ sudo nano $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
$ sudo nano $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
```

4. The shell scripts should be in the following format:

* For `activate.d`:

```
#!/bin/sh

export ENV_VAR='key'
export ENV_PATH=/path/to/my/credentials/
```

* For `deactivate.d`:

```
#!/bin/sh

unset ENV_VAR
unset ENV_PATH
```

* Now, whenever we run `conda activate env_name`, the environment variables will be set to the values stored in these files. On the flip side, running `conda deactivate` erases those variables.

5. To access these variables from Python:

```Python
import os

# To see all environment variables
os.environ

# To get specific environment variable
os.environ.get('ENV_VAR')

# Or
os.environ['ENV_VAR']
```

