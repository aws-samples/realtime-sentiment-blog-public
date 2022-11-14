# Instructions for creating the demo

## I. Create the stack using CloudFormation

### 1. Download the source code from the gitrepo

### 2. Create the S3 buckets to hold the CloudFormation template and source code
    a. 
    From AWS Console, create an s3 bucket to hold the cloud formation template (Bucket A, needed in step 3)
    Or, via AWS CLI:  
        aws s3api create-bucket --bucket [Bucket A] --region [REGION]

    b.
    Create a boto3 layer using the CLI as below (instructions for Unix OS)
        LIB_DIR=boto3-layer-targeted-sentiment/python
        mkdir -p $LIB_DIR
        pip3 install boto3 -t $LIB_DIR  (or your version of pip)
        cd boto3-layer-targeted-sentiment
        zip -r /tmp/boto3-layer-targeted-sentiment.zip .

    c. 
    From AWS Console, create an s3 bucket to hold the code (Bucket B) 
        i. Upload the sentiment-analysis-stepfunction.json to it
        ii. Upload the boto3-layer-targeted-sentiment.zip to it
    Or, via AWS CLI:
        i. aws s3api create-bucket --bucket [Bucket B] --region [REGION]
        ii. aws s3 cp sentiment-analysis-stepfunction.json s3://[Bucket B]
        iii. aws s3 cp boto3-layer-targeted-sentiment.zip s3://[Bucket B]

### 3. Deploy the CloudFormation template
   #### For the commands below, 
        Support Email Address:  Email where you want to receive the negative reviews
        Suffix:  A user supplied suffix to be used for the buckets created by CloudFormation. We need this to make sure your bucket names are unique

   #### In the root directory (where you downloaded the source code), type
    a. aws cloudformation package --template-file tots-cf-root.yaml --output-template packaged.yaml --s3-bucket [Bucket A]

    b. aws cloudformation deploy --template-file [current directory path]/packaged.yaml --stack-name tots-cf --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM CAPABILITY_NAMED_IAM --parameter-overrides Email=[Support email address] Suffix=[unique bucket suffix] CodeBucket=[Bucket B]

### 4.  Note the API endpoints 
#### After the deploy is successful, go to the API Gateway.
    Copy the two API endpoints from the Outputs tab of the API nested stack (starts with tots-cf-APIGateway-) and store it in your notepad
    a.  REST API endpoint:  Ends in "/enqueue"
    b.  CRM Tickets endpoint: Ends in "/targeted"

### 5. Update the API endpoint for the CRM Tickets page
    a. Locate the file showtable.js in the crm-tickets folder
    b. Modify line 19: apiGWUrl = '' and enter the API endpoint for CRM Tickets (ending in /targeted) copied from step above
    c. Save the file
    d. Copy the web page files from crm-tickets to S3://cf-realtime-sentiment-crm-tickets-[Suffix]
        For example,
        aws s3 cp crm-tickets/ s3://cf-realtime-sentiment-crm-tickets-[Suffix] --recursive 

### 6. Enable CORS for the CRM Tickets endpoint
   On the API Gateway, locate the endpoint ending in "/targeted", enable CORS.  Deploy API

### 7. Send sample reviews to API endpoint
#### Option 1: Actual reviews downloaded from Amazon Customer Reviews site
    Note:  Steps a-d have already been done for a sample review file.  You can proceed directly to    
            step e below.  If you want to download a fresh reviews file, start from step a
    a.  Visit the public site - Amazon Customer Reviews Dataset
    b.  Download a sample data set from S3, using AWS CLI.  For example, type
        aws s3 cp s3://amazon-reviews-pds/tsv/amazon_reviews_us_Camera_v1_00.tsv.gz .
    c.  Unzip the file and extract only the review text from this file
    d.  Save the file as amazon-customer-reviews.txt in the root directory
    e.  Run the python program sample-data-amazon-reviews.py in the root directory, to send         
        sample data to the API endpoint.  For example, type
            python ./sample-data-amazon-reviews.py (or use your version of python)
            When you are prompted to enter the API endpoint, enter the first endpoint (ending in /enqueue) copied from earlier step

#### Option 2: Simulated (mock) reviews on a Restaurant
    a. Run the python program sample-data.py in the root directory, to send sample data to the API    
       endpoint.  For example, type,
            python ./sample-data.py (or use your version of python)
            When you are prompted to enter the API endpoint, enter the first endpoint (ending in /enqueue) copied from earlier step

## II. Create QuickSight analysis

### 1.  Open QuickSight

### 2.  Give permissions to QuickSight to access the below S3 buckets
    Full Sentiment data is stored at:  cf-firehose-full-sentiment-bucket-[Suffix]
    Targeted Sentiment data is stored at: cf-firehose-targeted-sentiment-bucket-[Suffix]

### 3.  Analyses -> New Analyses -> New Dataset -> S3
    a.  Edit JSON file: ./quicksight-manifest/quicksight-full-sentiment-manifest.json
        Add suffix to the bucket after the last '-': s3://cf-firehose-full-sentiment-bucket-/

    b.  Datasource name: Full Sentiment Datasource
        JSON File: 
            Upload ./quicksight-manifest/quicksight-full-sentiment-manifest.json
        Click Connect

    c.  Create Pie chart for Total Sentiment
        Use dynamodb.NewImage.sentiment.S

    d.  Create vertical bar charts for 
        1. By Age Group (Use X axis = dynamodb.NewImage.sentiment.S and Y axis = dynamodb.NewImage.ageGroup.S)
        2. By Gender (Use X axis = dynamodb.NewImage.sentiment.S and Y axis = dynamodb.NewImage.gender.S)
        3. By State (Use X axis = dynamodb.NewImage.sentiment.S and Y axis = dynamodb.NewImage.state.S)

### 4.  Analyses -> New Analyses -> New Dataset -> S3
    a.  Edit JSON file: ./quicksight-manifest/quicksight-targ-sentiment-manifest.json
        Add suffix to the bucket after the last '-': s3://cf-firehose-targeted-sentiment-bucket-/

    b.  Datasource name: Targeted Sentiment Datasource
        JSON File: 
            Upload ./quicksight-manifest/quicksight-targ-sentiment-manifest.json
        Click Connect

    c.  Create stacked bar charts for 
        1. By Age Group (Use X axis = dynamodb.NewImage.sentiment.S and third dimension = dynamodb.NewImage.ageGroup.S)
        2. By Gender (Use X axis = dynamodb.NewImage.sentiment.S and third dimension = dynamodb.NewImage.gender.S)
        3. By State (Use X axis = dynamodb.NewImage.sentiment.S and third dimension = dynamodb.NewImage.state.S)

### 5.  Set refresh schedule to hourly for both datasets
    Click on the dataset, then the Refresh tab
    Add NEW SCHEDULE and set the schedule to Hourly


# III.  Test CRM Tickets feature
    a. Go to the CloudFront endpoint from the outputs tab of the CloudFront nested stack (starts with tots-cf-CloudFront-)

    b. If you have received an SNS notification on a negative sentiment, get the reviewId from the email
    This is the hex code that looks like this - 'b9c3xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    Enter it in the search box
    You will see the entities, sentiment and score corresponding to the sentiment.
    At this point you can create a ticket with a downstream CRM system (function not implemented, but shown as an example)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

