import psycopg2
import csv
import os

# Database connection parameters
db_name = 'citus'
db_user = 'citus'
db_password = 'mms2022MMS-'
db_host = 'c-vectorsearch.hfrtptuvsmgwws.postgres.cosmos.azure.com'

# File paths - update these with the paths to your files
details_file_path = 'C:/Users/mahmo/.vscode/video_process/detection_resultsGroof.csv'
vectors_file_path = 'C:/Users/mahmo/.vscode/video_process/vector_embeddingsGroof.csv'

# Establish a database connection
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
cursor = conn.cursor()

# Function to read vector file and convert vectors to the correct format
def read_vectors(file_path):
    vectors = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        for row in reader:
            # Ensure that each vector has 4096 elements
            if len(row) == 4096:
                vectors.append([float(v) for v in row])
            else:
                raise ValueError("Vector size mismatch")
    return vectors

# Function to read details file and insert data into the database
def insert_data(details_file_path, vectors):
    with open(details_file_path, 'r') as details_file:
        details_lines = details_file.readlines()[1:]  # Skip header

        
        for detail_line, vector in zip(details_lines, vectors):
            detail_parts = detail_line.strip().split(',')

            # Combine data
            combined_row = detail_parts + [vector]

            # SQL command for insertion
            insert_command = """
            INSERT INTO object_detection_data (vidId, frameNum, timestamp, detectedObjId, detectedObjClass, confidence, bbox_info, vector)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_command, combined_row)

    # Commit changes
    conn.commit()

# Read vector data
vectors = read_vectors(vectors_file_path)

# Insert data into the database
insert_data(details_file_path, vectors)

# Close the connection
cursor.close()
conn.close()
