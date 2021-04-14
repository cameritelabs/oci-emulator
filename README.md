# oci-emulator

![Generic badge](https://img.shields.io/badge/python-3.9.2-blue)
![Generic badge](https://img.shields.io/github/license/cameritelabs/oci-emulator)
![Generic badge](https://img.shields.io/badge/code%20style-black-000000.svg)

![Python application](https://github.com/cameritelabs/oci-emulator/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/cameritelabs/oci-emulator/branch/main/graph/badge.svg?token=5C8SX1Q6P9)](https://codecov.io/gh/cameritelabs/oci-emulator)

Oci-emualtor is an open source Oracle Cloud compatible server (emulator). Using python and flask, oci-emulator provides cross platform experiences for customers wanting to try Oracle Infrastructure in a local environment. Oci-emulator simulates some of the commands supported by Oracle Cloud with minimal dependencies.

## [DockerHub](https://hub.docker.com/r/cameritelabs/oci-emulator)

oci-emulator is available on dockerhub. To run it, just execute:

```bash
docker run -d -p 12000:12000 cameritelabs/oci-emulator:latest
```

## How to build?

### Using pyenv with pyenv-virtualenv

You also should use virtualenv to build/develop the project and I recommend the use of [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage multiple python environments.

```bash
pyenv update
pyenv install 3.9.2
pyenv virtualenv 3.9.2 oci-emulator
pyenv activate oci-emulator # in case your bash don't automatic activate
```

## Installing dependencies (Python 3.9.2)

Open your bash and run the following commands to install the required dependencies to run the project, you just need to run the command one time.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Instaling test dependencies (Python 3.9.2)

For testing and development, you'll need to download test dependencies. To do so, run the commands below on your bash:

```bash
python -m pip install -r test-requirements.txt
```

## Docker 🐋

Building the docker file:

```bash
docker build . -t cameritelabs/oci-emulator:latest
```

## How to Update a Local Fork at the Terminal/Command Line Interface

* Verify the remote branch attached for fetch and push operation using following command `git remote -v`.
* Specify a remote upstream repo to sync with your fork.

    ```bash
    git remote add upstream https://github.com/cameritelabs/oci-emulator.git
    ```

* Fetch branches and commits from the upstream repo. `git fetch upstream`.
* Checkout your fork’s local master using following command `git checkout main`.
* Merge changes from upstream/master into it `git merge upstream/master`.
* Push changes to update your fork master on Github `git push origin master`.

## Usage with Oracle SDKs

### Deafult authentication

To connect oci-emulator with the sdk, you have to provide the follow environment variable.

```txt
"USER" = "ocid1.user.oc1..testuser"
"FINGERPRINT" = "50:a6:c1:a1:da:71:57:dc:87:ae:90:af:9c:38:99:67"
"TENANCY" = "ocid1.tenancy.oc1..testtenancy"
"REGION" = "sa-saopaulo-1"
"KEY_FILE" = "assets/keys/private_key.pem"
"COMPARTMENT_ID" = "ocid1.compartment.oc1..testcompartment"
```

In some cases to use `Object Storage` you also need to provide `SERVICE_ENDPOINT`, in this cases needs to match with your docker url.
