# Note

## Comandi utili

### Package

#### Create package
* Creare il package ```tsppd``` nella cartella ```package```:
    ```bat
    py -m build
    ```

#### Run tests
* Installare il package ```pytest``` e dopo aver attivato il ```venv``` dentro i tests nella cartella ```package``` lanciare il comando:
    ```bat
    pytest tests
    ```
### CLI

* Creare un ```venv``` in python:
    ```bat
    rem All'interno della cartella di progetto
    python -m venv venv
    ```
* Attivare un ```venv``` in python:
    ```bat
    rem All'interno della cartella di progeto che contiene un venv
    venv\Scripts\activate.bat
    ```

* Installare la libreria ```tsppd``` nel progetto ```cli```:
    ```bat
    pip install C:\dev\TSP-con-pick-up-and-delivery\src\package\dist\tsppd-0.0.1-py3-none-any.whl --force-reinstall
    ```

* Usare la libreria ```tsppd``` nel progetto ```cli```:
    ```python
    import mypythonlib
    from mypythonlib import myfunctions
    ```