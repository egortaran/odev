# odev


### Configuring Environment Variables

1. Copy the **.env.template** file to **.env**
2. Open the **.env** file using a text editor.
3. Replace the placeholder values in the **.env** file with your own data. INFURA_KEY - your key on infura, PRIVATE_KEY - key for test transaction in pytest
4. Save the changes to the **.env** file.

### Installation on Windows

#### Create Python Virtual Environment and install requirements

    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

#### Run project

    python manage.py migrate
    python manage.py runserver
