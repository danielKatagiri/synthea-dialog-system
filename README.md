# synthea-dialog-system
A chatbot to talk with a FHIR R4 server


### Setup
For the application to run install the requirements and export your `OPENAI_API_KEY`.


### Initializing the Data Base
The chatbot interacts with a postgres database. To initialize the database
it is necessary to download the synthea sample data at:
[1K Sample Synthetic Patient Records, FHIR R4 ](https://mitre.box.com/shared/static/ylzmiichhvtw1igr4ck6q32i5b333nqs.zip)

After running the Docker Compose command, your database should be running at
http://localhost:5432 and ready to receive data. To insert the Synthea data into
the Postgres DB, simply run the following:
- export the env var SYNTHEA_FOLDER with the location where the synthea data is
located;
- Run the command: `python -m init_db`


### Initialize the chat room
The chat room was build using Streamlit's functionalities. To run the application
locally, run:

`streamlit run init_dialog_system.py`

Now you can test your application. Run questions like:
- What is the total patient count?
- What is the average age of the patients?
- What are the most common conditions?
