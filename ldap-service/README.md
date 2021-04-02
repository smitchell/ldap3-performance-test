# LDAP Service Demo

This is generic wrapper for LDAP3. I am looking at whether a generic template could be used for
OpenLDAP, Active Directory, Novell, etc where the only difference was logic to discover
and manage servers. The other reason for separating the microservices by backing service
would be to use vendor specific LDAP extensions.

A core principle of this POC is one microservice per LDAP backing service. Of course, this
could be done in a single LDAP microservice, but that would increase the complexity. 
Also, you could argue it would infringe on The Twelve Factors because deploying a bug fix 
for Active Directory could affect OpenLdap services too. 

## TECHNOLOGIES
This project uses the following libraries.
* Flask
* Ldap3
* Marshmallow
* Pytest
* Swagger
* Python Confuse

# RUNNING LOCALLY

## Local Configuration
The application configuration has been externalized. It is assumed that the environment specific configuration file is provided by a CI/CD 
pipeline when the image is deployed. Configurations are handled by [Python Confuse Library](https://confuse.readthedocs.io/en/latest/#). 
Python Confuse looks in these operation system locations under the application name:

* macOS: ~/.config/app or ~/Library/Application Support/app
* Other Unix: ~/.config/app and /etc/app
* Windows: %APPDATA%\app where the APPDATA environment variable falls back to %HOME%\AppData\Roaming if undefined

See the full documentation on [Python Confuse search Paths](https://confuse.readthedocs.io/en/latest/#search-paths).

Copy src/api/resource/config_template.yaml to the appropriate search path for your us in a directory named "ldap_service" named "config.yaml."
For macOS you could use "~/.config/ldap_service/config.yaml." For Windows you could use %APPDATA%\ldap_service\config.yaml."

```shell script
# macOS
mkdir ~/.config/ldap_service
###  OPTION A, if you need to edit the file for test or local with real passwords, OR... ###
cp $(pwd)/src/api/resources/config_template.yaml ~/.config/ldap_service/config.yaml

###  OPTION B, you can use a symbolic link if you only doing unit tests with the mock server and don't require a password  ###
ln -s $(pwd)/src/api/resources/config_template.yaml ~/.config/ldap_service/config.yaml

# Linux
mkdir /etc/ldap_service
cp ./src/ldap_service/resources/config_template.yaml /etc/ldap_service/config.yaml
```

# RUNNING IN DOCKER COMPOSE

When using Docker Compose in the parent directory the configuration rules above still apply inside the Docker container; however,
The two config files are copied from the ../configs directory one level above this directory.

## Host Names

The host names are defined in the Docker Compose, and referenced in the ../configs YAML files. If you run on K8S, pick your Service names
and then edit the host names in the ../configs YAML files to match.

For instance, in the ../configs/ldap_service.yml, change the ldap_host host URL to match the K8S Service name.
```
ldap_servers:
  test:
    description: Docker OpenLDAP server
    ldap_host: ldap://openldap-server
```

Likewise, update src/ldap/static/swapper.yaml and update the LDAP Service hostname:

```
servers:
  - url: http://localhost:5002
    description: Local testing
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
