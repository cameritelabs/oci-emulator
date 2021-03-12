# oci-emulator

<img src="https://img.shields.io/badge/python-3.9.2-blue"> <img src="https://img.shields.io/github/license/cameritelabs/oci-emulator">
![Python application](https://github.com/cameritelabs/oci-emulator/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/cameritelabs/oci-emulator/branch/main/graph/badge.svg?token=5C8SX1Q6P9)](https://codecov.io/gh/cameritelabs/oci-emulator)

oci-emulator is a mock of Oracle Cloud Infrastructure API using Flask. You can use it to test your application that integrates with OCI.

oci-emulator is available on dockerhub. To run it, just execute:
```
docker run -d -p 12000:12000 cameritelabs/oci-emulator:latest
```

## How to build?
### Using pyenv with pyenv-virtualenv

You also should use virtualenv to build/develop the project and I recommend the use of [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage multiple python environments.


```bash
pyenv update
pyenv install 3.9.2
pyenv virtualenv 3.9.2 oci-emulator
```

### Installing dependencies (Python 3.9.2)

Open your bash and run the following commands to install the required dependencies to run the project, you just need to run the command one time.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Instaling test dependencies (Python 3.9.2)

For testing and development, you'll need to download test dependencies. To do so, run the commands below on your bash:

```bash
python -m pip install -r test-requirements.txt
```

#### Docker 🐋

Building the docker file:
```bash
docker build . -t cameritelabs/oci-emulator:latest
```
