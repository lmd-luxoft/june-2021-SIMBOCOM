
Do the following changes in `feature_update_project_info` feature branch.

1. Update `README.md`:

   - fill project name
   - fill author name

2. Create virtual environment for Python 2:

For Linux:

```console
$ pip2 install --upgrade virtualenv
$ python2 -m virtualenv venv2
$ source venv2/bin/activate
$ pip install --upgrade pathlib
```

For Windows:

```console
> c:\Python27\python.exe -m pip install --upgrade virtualenv
> c:\Python27\python.exe -m virtualenv venv2
> venv2\Scripts\activate.bat
> c:\Python27\python.exe -m pip install --upgrade pip
> c:\Python27\python.exe -m pip install --upgrade wheel
> c:\Python27\python.exe -m pip install --upgrade pathlib
> pip install --upgrade -r requirements2.txt
```

3. Create `requirements.txt` file:

```text
pip
wheel
pathlib
```

Execute:

```console
$ pip install --upgrade -r requirements.txt
```

4. Add `.gitignore` file. Possible content is the following:

```gitignore
# python
__pycache__/
*.pyc

# virtual environment
.venv*/
venv*/
```
