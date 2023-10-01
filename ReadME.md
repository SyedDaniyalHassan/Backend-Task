Make the 'Backend-Task' as your current working Directory

Install All dependecies 
    `pip3 install requirments.txt`

Run the Server by following command:
    `uvicorn ForsitBackend.main:app`

For Database Connection, Set the Envoirment Variables, otherwise the Sqlite is the default database (can be isntalled by apt install sqlite3)

        DB_TYPE
        DB_USER
        DB_PASSWORD
        DB_HOST
        DB_PORT
        DB_NAME

For Populating the databse, thers is the sampleData.sql file, you can easily upload the sampleData in any database.

The SQLAlchemy ORM is used, so the schema will be created by its own when server starts.

THe Data Base Schema is also attached in the repo with the name, ForsitSchema.pdf