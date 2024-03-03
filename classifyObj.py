import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('./detection_resultsPreS.csv')

# Display the first few rows to understand the data structure
print(df.head())

# Analyze detected objects
print("Unique object classes detected:", df['detectedObjClass'].unique())
object_counts = df['detectedObjClass'].value_counts()
print("Counts of each object class detected:", object_counts)

# Visualize the distribution of detected objects
plt.figure(figsize=(10, 8))
object_counts.plot(kind='bar')
plt.title('Distribution of Detected Object Classes')
plt.xlabel('Object Class')
plt.ylabel('Counts')
plt.xticks(rotation=45)
plt.show()

# Assuming object_counts is a pandas Series from the previous example
with open('detection_resultsPreS.txt', 'w') as file:
    # Writing the header
    file.write("Counts of each object class detected:\n")
    
    # Iterating through the Series to write each class count
    for object_class, count in object_counts.items():
        file.write(f"{object_class}: {count}\n")
