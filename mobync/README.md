# Mobync

## Notes about documentation and contributing

If any substantial change is made, please, help out with the documentation.

## Run tests

```buildoutcfg
python3 -m unittest test
```

### Upgrading version on PyPI

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
