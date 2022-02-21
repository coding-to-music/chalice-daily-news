# Daily News Fetcher - How to Build a Serverless Application using AWS Chalice

# Build and deploy a Python based serverless REST API in no time

By Siben Nayak

https://towardsdatascience.com/how-to-build-a-serverless-application-using-aws-chalice-91024416d84f

https://github.com/theawesomenayak/daily-news/blob/main/app.py

Oct 14, 2020·4 min read

![image](https://user-images.githubusercontent.com/3156358/154875111-67dfbc6d-8b1a-4be0-9fc9-88358d1fbef7.png)

Image by Author. Original image by Pixabay via Canva

I recently came across AWS Chalice and was fascinated by the simplicity and usability offered by it. AWS Chalice is a serverless framework that allows you to build serverless applications using Python, and deploy them on AWS using Amazon API Gateway and AWS Lambda.
I decided to play around with it and was actually able to create and deploy a sample REST API on AWS within a few minutes. In this article, I will walk you through the steps required to build and deploy a serverless application that gets the latest news from Google News using AWS Chalice.

# Prerequisites

This tutorial requires an AWS account. If you don’t have one already, go ahead and create one. Our application is going to use only the free-tier resources, so cost shouldn’t be an issue. You also need to configure security and create users and roles for your access.
Configuring AWS Credentials
Chalice uses AWS Command Line Interface (CLI) behind the scenes to deploy the project. If you haven’t used AWS CLI before to work with AWS resources, you can install it by following the guidelines here.
Once installed, you need to configure your AWS CLI to use the credentials from your AWS account.

```java
$ aws configure
AWS Access Key ID [****************OI3G]:
AWS Secret Access Key [****************weRu]:
Default region name [us-west-2]:
Default output format [None]:
```

## Installing Chalice

Next, you need to install Chalice. We will be using Python 3 in this tutorial, but you can use any version of Python supported by AWS Lambda.

## Verify Python Installation

```java
$ python3 --version
Python 3.8.6
Install Chalice
$ python3 -m pip install chalice
```

## Verify Chalice Installation

```java
$ chalice --version
chalice 1.20.0, python 3.8.6, darwin 19.6.0
```

## Creating a Project

Next, run the chalice command to create a new project:

```java
$ chalice new-project daily-news
```

This will create a daily-news folder in your current directory. You can see that Chalice has created several files in this folder.

![image](https://user-images.githubusercontent.com/3156358/154875485-1c2acdbd-c7d8-45e6-8c0b-3f8ffe2b8828.png)

Image by Author

Let’s take a look at the app.py file:

The new-project command created a sample app that defines a single view, / that returns the JSON body {"hello": "world"} when called. You can now modify this template and add more code to read news from Google.
We will be using Google’s RSS feed, and will need a Python library called Beautiful Soup for parsing the XML data. You can install Beautiful Soup and its XML parsing library using pip.

```java
$ python3 -m pip install bs4
$ python3 -m pip install lxml
```

Next add the following imports to app.py. This essentially adds imports from urllib to make HTTP calls and bs4 to parse XML.

Next, you need to add a method to fetch the RSS feed from Google, parse it to extract the news title and publication date, and create a list of news items. To do this, add the following code to your app.py

Update the index method in app.py to invoke this and return the list of news items as result.

Note that you installed a few dependencies to make the code work. These dependencies were installed locally, and will not be available to the AWS Lambda container at runtime. To make them available to AWS Lambda, you will need to package them along with your code. To do that, add the following to the requirements.txt file. Chalice packs these dependencies as part of your code during build and uploads them as part of the Lambda function.

# Deploying the Project

Let’s deploy this app. From the daily-news folder, run the chalice deploy command.

![image](https://user-images.githubusercontent.com/3156358/154875438-bfef59c0-ccc3-4f45-9d0e-4548a5f7e9f3.png)

Deployment (Image by Author)

This deploys your API on AWS using Amazon API Gateway and AWS Lambda.

daily-news API in API Gateway (Image by Author)

![image](https://user-images.githubusercontent.com/3156358/154875411-94987f0d-d814-4371-9a94-0ec4eb58c272.png)

daily-news-dev Lambda Function (Image by Author)

You can now try accessing the API.

![image](https://user-images.githubusercontent.com/3156358/154875323-c67a19be-7642-4069-ae8b-53afc8e051dd.png)

Calling the news API (Image by Author)

# Cleaning Up

You can also use the chalice delete command to delete all the resources created when you ran the chalice deploy command.

Deleting Resources (Image by Author)

# Conclusion

Congratulations!! You just deployed a serverless application on AWS using Chalice. It wasn’t too hard, was it?
You can now go ahead and make any modifications to your app.py file and rerun chalice deploy to redeploy your changes.

You can also use Chalice to integrate your serverless app with Amazon S3, Amazon SNS, Amazon SQS, and other AWS services. Take a look at the tutorials and keep exploring.
The full source code for this tutorial can be found here.

https://github.com/theawesomenayak/daily-news/blob/main/app.py
