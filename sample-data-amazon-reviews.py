import random
import json
import os
from string import punctuation

def remove_non_alnumspace(string):
    #no &, ', %
    allowedChars = [' ', '!', '@', '#', '$', '^', '*', '*', '(', ')', '-', '+', '_', '=', ':', ';', ',', '<', '>', '.', '?', '/']
    return ''.join(char for char in string if (char.isalnum() or char in allowedChars))

pathToReviewsFile = "./amazon-customer-reviews.txt"

state=["NY", "NJ", "CT", "PA", "CA"]
wstate=[1,1,1,1,1]

ageGroup=["TEEN", "YOUNG ADULT", "ADULT", "SENIOR"]
wageGroup=[1,1,1,1]

gender=["MALE", "FEMALE"]
wgender=[1,1]

alpha=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

with open(pathToReviewsFile) as f:
   reviews=f.readlines()

numReviews = len(reviews)
numSamples=10

if (len(reviews) < numSamples):
    print('Number of reviews {} is less than the number of samples {}'.format(numReviews, numSamples))
    exit

indices = random.sample(range(numReviews), numSamples)

endpoint = input("Enpoint (ending in /enqueue): ")

for i in range(0, numSamples):
    stix = random.choices(state, weights = wstate, k = 1)
    agix = random.choices(ageGroup, weights = wageGroup, k = 1)
    gdix = random.choices(gender, weights = wgender, k = 1)

    aix = random.choice(alpha)
    author = aix[0] + str(random.randint(1, 100000)) + "@abc.com"

    review = reviews[indices[i]]
    review = remove_non_alnumspace(review)
    data = {
        "review" : review,
        "author" : author,
        "ageGroup" : agix[0],
        "gender" : gdix[0],
        "state" : stix[0]
    }

    curlCmd = "curl -X POST -H 'Content-Type: application/json' -d '" + json.dumps(data) + "' " + endpoint
    print('POST #{}: {}'.format(i+1,curlCmd))
    os.system(curlCmd)
    print('\n\n')
