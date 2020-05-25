import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import datetime

TEST_SIZE = 0.4

MONTH_DICT = {
    'Jan':0,
    'Feb':1,
    'Mar':2,
    'Apr':3,
    'May':4,
    'June':5,
    'Jul':6,
    'Aug':7,
    'Sep':8,
    'Oct':9,
    'Nov':10,
    'Dec':11
}

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            data.append({
                "evidence": [
                    int(row[0]),
                    float(row[1]),
                    int(row[2]),
                    float(row[3]),
                    int(row[4])
                ]+\
                [float(cell) for cell in row[5:10]]+\
                [int(MONTH_DICT[row[10]])]+\
                [int(cell) for cell in row[11:15]]+\
                [
                    1 if row[15] == 'Returning_Visitor' else 0,
                    int(row[16] ==  'TRUE')
                ],
                "label": int(row[17] == 'TRUE')
            })
    

    # Separate data into training and testing groups
    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=5).fit(evidence, labels)
    
    return model
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    correct_positive = 0
    correct_negative = 0

    for i in range(len(labels)):
        if labels[i] == predictions[i] == 1:
            correct_positive += 1
        if labels[i] == predictions[i] == 0:
            correct_negative += 1
    
    total_positive = sum(labels)
    total_negative = len(labels) - total_positive
    
    sensitivity = correct_positive/total_positive
    specificity = correct_negative/total_negative
    
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
