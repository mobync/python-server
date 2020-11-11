# Contributing to Mobync

## Introduction

This is the mobync server implementation for python.

If your backend uses another language, please verify if it's available on [Mobync repositories](https://github.com/mobync/).

If you need a mobync in a language not supported yet, feel free to contact us to make the suggestion, or take the initiative and helps us by contributing to this new mobync implementation.

## Documentation and contributing

Feel free to propose improvements, open issues, or pull requests.

If any substantial change is made, please, help out with the documentation.

## Understanding how mobync works

### The user implements an interface for mobync

The user implements the mobync Synchronize class interface.

With the methods on that class, mobync will be able to access the user database and validate the user data.

```python
import abc
from typing import List

from mobync import ReadFilter


class Synchronizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self, where: str, filters: List[ReadFilter]) -> str:
        pass

    @abc.abstractmethod
    def update(self, where: str, data_json: str) -> None:
        pass

    @abc.abstractmethod
    def validate_update(self, owner_id: str, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def create(self, where: str, data_json: str) -> None:  # todo: should receive dict?
        pass

    @abc.abstractmethod
    def validate_create(self, owner_id: str, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def delete(self, where: str, data_json: str) -> None:
        pass

    @abc.abstractmethod
    def validate_delete(self, owner_id: str, **kwargs) -> bool:
        pass
```

### The user will implement a Sync API endpoint

When data coming from the user frontend hit the sync endpoint 

### The Sync process

#### First the data is validated

#### Then simplified, merged with diffs on server

#### applied on server

#### sent back to frontend with what needs to be applied there

## Run tests

To run the tests locally:

```bash
python -m unittest tests/test_mobync_implementation.py
python -m unittest tests/test_client_integration.py
```

### Creating new tests

If any new feature is added, please consider creating new tests on the test folder and add them travis pipeline on `.travis.yml`.

## Uploading a new version on PyPI

Make sure you have the latest versions of setuptools and wheel installed:

```
pip install twine
```

Now run this command from the same directory where setup.py is located:

```
python setup.py sdist bdist_wheel
```

This command will generate a file in the dist directory.

Run Twine to upload all of the archives under dist:

```
twine upload dist/*
```

You will be asked your username and password from your Pypi account, in which you must have access to the project to upload.

After this, the version on Pypi is already updated. 

Now you should delete the dist folder:

```
rm -rf dist/
```
