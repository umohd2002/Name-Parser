from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from ORM import ClueTable

# Define your SQLAlchemy table
Base = declarative_base()
# Replace 'sqlite:///your_database.db' with your actual database connection string
engine = create_engine('sqlite:///KnowledgeBase.db')
# Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Path to your data file
file_path = 'NameClueTable_1.txt'

# Read the data file and insert into the database
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split('|')
            if len(parts) == 2:
                abbreviation = parts[0].strip()
                expansion = parts[1].strip()

                # Create an instance of the ClueTable
                clue_instance = ClueTable(component_desc=abbreviation, token=expansion)

                # Add the instance to the session
                try:
                    session.add(clue_instance)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    print(f"Skipping duplicate entry: {abbreviation} - {expansion}")

# Close the session
session.close()


# # Import the necessary modules
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from ORM import MapCreationTable, ExceptionTable, ClueTable  # Replace 'your_module_name' with the actual module name

# # Create an engine
# engine = create_engine('sqlite:///KnowledgeBase.db')

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Empty the 'mapCreationTable'
# session.query(ClueTable).delete()


# # Commit the changes
# session.commit()

# # Close the session
# session.close()
