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

```java
from chalice import Chalice

app = Chalice(app_name='daily-news')


@app.route('/')
def index():
    return {'hello': 'world'}
```

The new-project command created a sample app that defines a single view, / that returns the JSON body {"hello": "world"} when called. You can now modify this template and add more code to read news from Google.
We will be using Google’s RSS feed, and will need a Python library called Beautiful Soup for parsing the XML data. You can install Beautiful Soup and its XML parsing library using pip.

```java
$ python3 -m pip install bs4
$ python3 -m pip install lxml
```

Next add the following imports to app.py. This essentially adds imports from urllib to make HTTP calls and bs4 to parse XML.

```java
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

news_url = "https://news.google.com/news/rss"
```

Next, you need to add a method to fetch the RSS feed from Google, parse it to extract the news title and publication date, and create a list of news items. To do this, add the following code to your app.py

```java
def get_news_from_google():
    client = urlopen(news_url)
    page = client.read()
    client.close()
    souped = soup(page, "xml")
    news_list = souped.findAll("item")
    result = []
    for news in news_list:
        data = {}
        data['title'] = news.title.text
        data['date'] = news.pubDate.text
        result.append(data)
    return result
```

Update the index method in app.py to invoke this and return the list of news items as result.

```java
@app.route('/news')
def index():
    news = get_news_from_google()
    return {'result': news}
```

Note that you installed a few dependencies to make the code work. These dependencies were installed locally, and will not be available to the AWS Lambda container at runtime. To make them available to AWS Lambda, you will need to package them along with your code. To do that, add the following to the requirements.txt file. Chalice packs these dependencies as part of your code during build and uploads them as part of the Lambda function.

The final code should look like this:

```java


from chalice import Chalice
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

news_url = "https://news.google.com/news/rss"
app = Chalice(app_name='daily-news')

@app.route('/news')
def index():
    news = get_news_from_google()
    return {'result': news}


def get_news_from_google():
    client = urlopen(news_url)
    page = client.read()
    client.close()
    souped = soup(page, "xml")
    news_list = souped.findAll("item")
    result = []
    for news in news_list:
        data = {}
        data['title'] = news.title.text
        data['date'] = news.pubDate.text
        result.append(data)
    return result
```

```java
pip freeze | grep "beautifulsoup4" >>  requirements.txt
pip freeze | grep "bs4" >>  requirements.txt
pip freeze | grep "soupsieve" >>  requirements.txt
pip freeze | grep "lxml" >>  requirements.txt
```

```java
beautifulsoup4==4.8.2
bs4==0.0.1
soupsieve==1.9.5
lxml==4.5.0
```

# Deploying the Project

Let’s deploy this app. From the daily-news folder, run the chalice deploy command.

```java
chalice deploy
```

![image](https://user-images.githubusercontent.com/3156358/154875438-bfef59c0-ccc3-4f45-9d0e-4548a5f7e9f3.png)

Deployment (Image by Author)

## Here is my deployment error

```java
/usr/local/lib/python3.8/dist-packages/_distutils_hack/__init__.py:36: UserWarning: Setuptools is replacing distutils.
  warnings.warn("Setuptools is replacing distutils.")
Creating deployment package.
Reusing existing deployment package.
Updating policy for IAM role: chalice-daily-news-dev
Creating lambda function: chalice-daily-news-dev
Traceback (most recent call last):
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/cli/__init__.py", line 636, in main
    return cli(obj={})
  File "/usr/lib/python3/dist-packages/click/core.py", line 764, in __call__
    return self.main(*args, **kwargs)
  File "/usr/lib/python3/dist-packages/click/core.py", line 717, in main
    rv = self.invoke(ctx)
  File "/usr/lib/python3/dist-packages/click/core.py", line 1137, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/usr/lib/python3/dist-packages/click/core.py", line 956, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/usr/lib/python3/dist-packages/click/core.py", line 555, in invoke
    return callback(*args, **kwargs)
  File "/usr/lib/python3/dist-packages/click/decorators.py", line 17, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/cli/__init__.py", line 189, in deploy
    deployed_values = d.deploy(config, chalice_stage_name=stage)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/deploy/deployer.py", line 376, in deploy
    return self._deploy(config, chalice_stage_name)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/deploy/deployer.py", line 392, in _deploy
    self._executor.execute(plan)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/deploy/executor.py", line 42, in execute
    getattr(self, '_do_%s' % instruction.__class__.__name__.lower(),
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/deploy/executor.py", line 55, in _do_apicall
    result = method(**final_kwargs)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/awsclient.py", line 408, in create_function
    arn, state = self._create_lambda_function(kwargs)
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/awsclient.py", line 575, in _create_lambda_function
    result = self._call_client_method_with_retries(
  File "/home/tmc/.local/lib/python3.8/site-packages/chalice/awsclient.py", line 1890, in _call_client_method_with_retries
    client.exceptions.ResourceInUseException,
  File "/home/tmc/.local/lib/python3.8/site-packages/botocore/errorfactory.py", line 51, in __getattr__
    raise AttributeError(

AttributeError: <botocore.errorfactory.LambdaExceptions object at 0x7f1ed11ac3d0>
object has no attribute 'ResourceInUseException'.

Valid exceptions are:
CodeStorageExceededException,
EC2AccessDeniedException,
EC2ThrottledException,
EC2UnexpectedException,
ENILimitReachedException,
InvalidParameterValueException,
InvalidRequestContentException,
InvalidRuntimeException,
InvalidSecurityGroupIDException,
InvalidSubnetIDException,
InvalidZipFileException,
KMSAccessDeniedException,
KMSDisabledException,
KMSInvalidStateException,
KMSNotFoundException,
PolicyLengthExceededException,
RequestTooLargeException,
ResourceConflictException,
ResourceNotFoundException,
ServiceException,
SubnetIPAddressLimitReachedException,
TooManyRequestsException,
UnsupportedMediaTypeException
```

This deploys your API on AWS using Amazon API Gateway and AWS Lambda.

daily-news API in API Gateway (Image by Author)

![image](https://user-images.githubusercontent.com/3156358/154875411-94987f0d-d814-4371-9a94-0ec4eb58c272.png)

daily-news-dev Lambda Function (Image by Author)

You can now try accessing the API.

![image](https://user-images.githubusercontent.com/3156358/154875323-c67a19be-7642-4069-ae8b-53afc8e051dd.png)

Calling the news API (Image by Author)

# Cleaning Up

You can also use the chalice delete command to delete all the resources created when you ran the chalice deploy command.

![image](https://user-images.githubusercontent.com/3156358/154881697-9531e88b-0d57-4361-bd59-6bb625237034.png)

Deleting Resources (Image by Author)

# Conclusion

Congratulations!! You just deployed a serverless application on AWS using Chalice. It wasn’t too hard, was it?
You can now go ahead and make any modifications to your app.py file and rerun chalice deploy to redeploy your changes.

You can also use Chalice to integrate your serverless app with Amazon S3, Amazon SNS, Amazon SQS, and other AWS services. Take a look at the tutorials and keep exploring.
The full source code for this tutorial can be found here.

https://github.com/theawesomenayak/daily-news/blob/main/app.py
