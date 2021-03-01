# Gateway Demo

## TECHNOLOGIES
This project uses the following libraries.
* Flask
* Marshmallow
* Pytest
* Swagger
* Python Confuse

## RUNNING LOCALLY

### Configuration
The application configuration has been externalized. It is assumed that the environment specific configuration file is provided by a CI/CD 
pipeline when the image is deployed. Configurations are handled by [Python Confuse Library](https://confuse.readthedocs.io/en/latest/#). 
Python Confuse looks in these operation system locations under the application name:

* macOS: ~/.config/app or ~/Library/Application Support/app
* Other Unix: ~/.config/app and /etc/app
* Windows: %APPDATA%\app where the APPDATA environment variable falls back to %HOME%\AppData\Roaming if undefined

See the full documentation on [Python Confuse search Paths](https://confuse.readthedocs.io/en/latest/#search-paths).

Copy app/src/gateway/resource/config_template.yaml to the appropriate search path for your us in a directory named "gateway_service" named "config.yaml."
For macOS you could use "~/.config/gateway_service/config.yaml." For Windows you could use %APPDATA%\gateway_service\config.yaml."

```shell script
# macOS
mkdir ~/.config/gateway_service
###  OPTION A, if you need to edit the file for test or local with real passwords, OR... ###
cp $(pwd)/app/src/gateway/resources/config_template.yaml ~/.config/gateway_service/config.yaml

###  OPTION B, you can use a symbolic link if you only doing unit tests with the mock server and don't require a password  ###
ln -s $(pwd)/app/src/gateway/resources/config_template.yaml ~/.config/gateway_service/config.yaml

# Linux
mkdir /etc/gateway_service
cp ./app/src/gateway/resources/config_template.yaml /etc/gateway_service/config.yaml
```

### Running tests or Swagger

1) python3 -m venv --copies venv
1) source venv/bin/activate
1) cd app
1) pip install -r requirements.txt
1) pip install .
1) pytest
1) make run
8) http://localhost:5000/api/docs

# RESOURCES
These are the references I used in structuring this project. Full disclosure, I wrote Java
for 20 years, so you won't find a models.py file. I give every class its own file and
it's own test file.

I started with [Martin Heinz's](https://martinheinz.dev/) project blueprint, folded in ideas from 
[Sean Bradley's](https://github.com/Sean-Bradley) Flask Rest boilerplate, and then I refactored the project test packaging 
as proposed by [Ionel Cristian Mărieș](https://blog.ionelmc.ro/about/).

* https://github.com/ionelmc/cookiecutter-pylibrary
* https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
* https://towardsdatascience.com/ultimate-setup-for-your-next-python-project-179bda8a7c2c
* https://github.com/Sean-Bradley/Seans-Python3-Flask-Rest-Boilerplate
* https://github.com/MartinHeinz/python-project-blueprint
