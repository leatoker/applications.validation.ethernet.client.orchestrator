# flask-sso
This is a sample Flask application that

* uses IAM Web Services Interface
to identify and authenticate its web users (one per session)
* validates an authorization for the user
* displays results on its main page

It was developed as an elaboration
on [Python-IAMWS-Lib](https://github.intel.com/SecurityDev/Python-IAMWS-Lib)

The main additions were
* define in a separate file a Python service to use the IAM WS
* add comments in the code explaining what happens on each step
* add code to handle exceptions, hopefully most useful 
for the first times this demo is used, before it is copied into a
larger app.
* add self-generated certs to enable running it locally
* parameterize URLs and other constants
* include a couple of scripts to deploy the app in Cloud Foundry, if desired

## How to use it
1. Clone the repo on your local system
2. Complete the user **Account Requirements** (below) 
3. Create a Python environment and install the requirements:
    ```bash
    $ pip install -r requirements.txt
    ``` 
4. Run the app
    ```bash
    $ python flask-sso.py
    ``` 

## Account Requirements
Copied from the original [source](https://github.intel.com/SecurityDev/Python-IAMWS-Lib).

### Prerequisites

* Each application should create and register their own system account
(e.g. sys_appname) with Intel IAM Web Service.
See the next section for instructions.
This account and password should be used for getting an access token from
Intel IAM Web Service.
It is possible to create a system account for exploration projects
using the following naming convention: sys_username (e.g. sys_apulver).

* The application should be accessible from an external host - the authentication flow
involves a redirect to Intel IAM Web Service that in turn redirects back
to the application.
    * The host running the application should have a proper TLS/SSL
certificate - Intel IAM Web Service always redirects back to the application using HTTPS
scheme (regardless of whether developer specified HTTP or HTTPS).
    * You can deploy this example on Intel Cloud Application Platform
(http://goto/cloudservices => Applications) and that takes care of that for you.
    * _To run locally, you can follow the section below called
    "How to generate a TLS cert and key for the app"_

* Intel IAM Web Service team kindly asks to cache the access token
until it is expired. That is automatically handled by the iamws service module
in this repository.

### Registering system account with Intel IAM Web Service

Intel IAM Web Service requires a generic account from Global Request System,
application name from Intel Application Profiler and relevant role in Intel Access Governance System.

To request access:

1. http://goto/globalrequest => Network/Email Accounts => New Request =>
Generic Network and Email =>
Create (request type: "Create Network Account with Email"; prefix: "sys_")
2. http://goto/passreset => CORP Faceless account => Reset password
3. http://goto/ags => IDENTITIES => Manage Generic Accounts =>
Update Generic Account => Choose your account from "Login ID" dropdown menu => Next =>
Update mandatory fields => Next => Submit
1. http://goto/ags => ACCESS => Submit Requests => For Others =>
d your account, select it and click "Submit" =>
rch for **"IAM WS-I Token_WindowsAuth Scope"** role
nd "IAM WS-I Authorizations Scope"** =>
 To Cart => Checkout => Add justification => Submit

## How to generate a TLS cert and key for the app

Following [Running Your Flask Application Over HTTPS](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

Generate a self-signed cert:

```bash
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

This command writes a new certificate in `cert.pem` with its
corresponding private key in `key.pem` 
and with a validity of 365 days.

When you run this command, you will be asked a few questions.
Below you can see how I answered them to generate a certificate
for calang-mobl.amr.corp.intel.com:

```
Generating a 4096 bit RSA private key
......................++
.............++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CR
State or Province Name (full name) [Some-State]:Heredia
Locality Name (eg, city) []:Belen
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Intel
Organizational Unit Name (eg, section) []:Enterprise Analytics
Common Name (e.g. server FQDN or YOUR name) []:calang-mobl.amr.corp.intel.com
Email Address []:carlos.a.lang@intel.com
```

## Notes
1. It's OK to use self-signed certificates for development but 
[pki services](http://pki.intel.com) should be used in production.
1. Session key encryption should be strengthen to meet
production requirements

## Key Files
* **cf_config** - sets Linux configuration variables to allow deployment
in Cloud Foundry
* **cf_login** - Linux script to log into CF
* **cf_push** - Linux script to push your app into CF
* **flask-sso.py** - Flask API server application
* **iamws.py** - module implementing a service to use the IAM WS API
* **manifest.yml** - app configuration file to deploy in CF
* **Procfile** - CF spec file on how to run the app once deployed
* **requirements.txt** - list of packages required to install the app
* **runtime.txt** - spec file with the Python version to use
* **vars-template.yml** - template file indicating how to produce a
**vars.yml** file, storing the secrets required to run the application
 
## References
* IAM WS API user manual: http://goto.intel.com/iamwsapi
* https://github.intel.com/SecurityDev/Python-IAMWS-Lib
* Authentication & Authorization using AGS and IAM WS for
Internal Applications Step-by-Step Guide - https://github.intel.com/gist/psalessi/85a23640eb75d83c4a5e 
