# odev


### Configuring Environment Variables

1. Copy the **.env.template** file to **.env**
2. Open the **.env** file using a text editor.
3. Replace the placeholder values in the **.env** file with your own data. INFURA_KEY - your key on infura, PRIVATE_KEY - private key wallet for test transaction in pytest
4. Save the changes to the **.env** file.

### Installation on Windows

#### Create Python Virtual Environment and install requirements

    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

#### Run project

    python manage.py migrate
    python manage.py runserver

### Comments on the work
1. I didn't spend much time for API documentation
2. Gas-based validation is not configured
3. I used the sepolia network
4. In order for the tests to be successful, you must enter PRIVATE_KEY in the .env file. The test transaction uses 0.0001 ETH, gas = 21000 and gasPrice = 50 gwei in sepolia network
5. For start test you should write **pytest** in main directory
6. To see the API documentation, go to api/schema/swagger-ui/
