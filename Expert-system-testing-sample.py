import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

# Initial data
base_data = {
    'appetite_loss': 'yes', 
    'fever': 'no',
    'short_breath': 'no',
    'fatigue': 'no',
    'joint_pain': 'yes',
    'vomits': 'no'
}

# Generate 500 similar entries
generated_data = []
for _ in range(500):
    entry = base_data.copy()
    for key in entry:
        # Randomly switch 'yes' to 'no' and vice versa
        if random.choice([True, False]):
            entry[key] = 'yes' if entry[key] == 'no' else 'no'
    generated_data.append(entry)

# Print the first few entries
for i in range(5):
    print(f"Entry {i + 1}: {generated_data[i]}")


#Testing the system code

# Assuming a binary classification problem
target_variable = ['yes', 'no']

# Assuming 'disease' as a hypothetical target variable
generated_data_with_labels = [{'disease': random.choice(target_variable), **entry} for entry in generated_data]

# Convert features and labels to a DataFrame
df = pd.DataFrame(generated_data_with_labels)

# Extract features and labels
X = df.drop('disease', axis=1)
y = df['disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a transformer to one-hot encode categorical features
categorical_features = list(X_train.columns)
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_features)])

# Create a pipeline with the transformer and the classifier
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', DecisionTreeClassifier(random_state=42))])

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100}%")