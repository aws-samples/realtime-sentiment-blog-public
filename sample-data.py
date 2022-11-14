import random
import json
import os

#The restaurant in [state] was [ambience].  The [food] was [sentiment].  The service was [service]

food=["pasta", "salad", "bread", "meat", "dessert", "main course", "soup"]
wfood=[1,1,1,1,1,1,1]

state=["NY", "NJ", "CT", "PA", "CA"]
wstate=[1,1,1,1,1]

appearance=["wonderful", "spacious",  "trendy", "tiny", "crowded", "very old"]
wappearance=[1,1,1,1,1,1]

sentiment=["excellent", "very good", "good", "OK", "bad", "terrible"]
wsentiment=[1,1,1,1,1,1]

service=["excellent", "very good", "good", "OK", "bad", "very bad"]
wservice=[1,1,1,1,1,1]

entityTypes=["ambience", "location", "food"]

ageGroup=["TEEN", "YOUNG ADULT", "ADULT", "SENIOR"]
wageGroup=[1,1,1,1]

gender=["MALE", "FEMALE"]
wgender=[1,1]

alpha=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

numSamples=10
negativeSentimentBias=True

endpoint = input("Enpoint: ")

for i in range(1, numSamples):
    foix = random.choices(food, weights = wfood, k = 1)
    stix = random.choices(state, weights = wstate, k = 1)
    apix = random.choices(appearance, weights = wappearance, k = 1)
    snix = random.choices(sentiment, weights = wsentiment, k = 1)
    svix = random.choices(service, weights = wservice, k = 1)
    agix = random.choices(ageGroup, weights = wageGroup, k = 1)
    gdix = random.choices(gender, weights = wgender, k = 1)

    aix = random.choice(alpha)
    author = aix[0] + str(random.randint(1, 100000)) + "@abc.com"

    review = "The restaurant in {} was {}. The {} was {}.  The service was {}".format(stix[0], apix[0], foix[0], snix[0], svix[0])
    data = {
        "review" : review,
        "author" : author,
        "ageGroup" : agix[0],
        "gender" : gdix[0],
        "state" : stix[0]
    }

    curlCmd = "curl -X POST -H 'Content-Type: application/json' -d '" + json.dumps(data) + "' " + endpoint
    print(curlCmd)
    os.system(curlCmd)
    print()
