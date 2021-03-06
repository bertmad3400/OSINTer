# OSINTer
[![OSINTer](https://gitlab.com/osinter/osinter/raw/master/logo.png)](https://osinter.dk)

## *Looking for help*
OSINTer has grown a lot the last few months, and after adopting a new backend powered by Elasticsearch, it has become able to handle very large amounts of data. Therefore we are currently looking into machine learning for doing a bit of data analysis (specifically text summarization and data clustering), but unfortunately my knowledge on the subject is rather sparse. Therefore, if you're data scientist/analysis, or programmer who has a hold these subjects, and would like to contribute to OSINTer, please reach out on skrivtilbertram@gmail.com. As the project is free and open-source (and I'm doing the development unpaid) I unfortunately do not have the possibility of paying for your work, but at least there's plenty of currated real-world data and interresting challenges.

## Contributing
As OSINTer is open-source we highly encourage any form of contributing under the current license in the relevant parts of the project. Should you want to contribute, then this is done either by sending the patches manually over email to skrivtilbertram@gmail.com, or by utilizing the [Gitlab platform](https://gitlab.com/osinter) to submit pull requests (if you're reading this on Github, then that's merely a downstream mirror of the Gitlab repositories).

## Introduction
OSINTer is an open source intelligence gathering tool, designed to ease the intelligence gathering process by scraping reliable intelligence news sources, and presenting them in an easy to navigate UI, hosted as a webserver, to allow intelligence analysts to look at a great deal of intelligence collectively.

OSINTer is split into multiple repositories for ease of development, listed below:
| Repository | Description |
| --- | --- |
| [OSINTansible](https://gitlab.com/osinter/ansible) | Responsible for making the installation process easier, by using ansible. |
| [OSINTbackend](https://gitlab.com/osinter/backend) | Responsible for the scraping and initialization of OSINTer. |
| [OSINTmodules](https://gitlab.com/osinter/modules) | Responsible for handling many of the finer operations, such as the scraping, text handling, and DBMS. |
| [OSINTprofiles](https://gitlab.com/osinter/profiles) | Responsible for specifying the various sources that are scraped for intelligence. |
| [OSINTwebserver](https://gitlab.com/osinter/webserver) | Responsible for displaying the intelligence in an easy to view format.|
| [OSINTblog](https://gitlab.com/osinter/blog) | Responsible for the software and content at the blog associated with OSINTer |


 For a demonstration of how it looks and works, have a look at our demo-site at [OSINTer.dk](https://osinter.dk)

## What problem does OSINTer attempt to solve?
The process of gathering cyber threat intelligence is only as successful as the investigators ability to identify relevant intelligence sources. Identifying relevant and reliable sources could often be a time-consuming task, as the CTI personnel would have to first locate the intelligence source, then read it to identify its relevance and usefulness as well as identify its formatting, and finally mark down all relevant details for usage in their report. This is time consuming and can be hit and miss depending on the skill and experience of the CTI personnel, and while products to combat this repetitive and time-consuming task, like Recorded Future, exists, these are often not only expensive, but also closed in nature, as they rarely integrate well with thirdparty utilities.

The goal of OSINTer is to build an open-source and extensible platform for collecting and organizing open-source intelligence in a way that easily intergrates with thirdparty utilities and other pieces of open-source software. As such, it never was (and never will be) intended to compete with products like the aforementioned Recorded Future, since the core concept is very different and since OSINTer does not offer the needed analysis capabilities on its own.


## How does OSINTer Solve the Problem?
Firstly, to combat the time-consuming task of identifying relevant threat intelligence sources, OSINTer gathers information from known, reliable sources, automatically, and then displays these in its webservice interface in a list sorted by publish date. This provides the most current information first, and in a consistent format so that users can easily identify the relevant information sources for their CTI reports or other use cases.

Secondly, the content from the threat intelligence sources is archived and retrievable for the user, through a download functionality in OSINTer, which allows for download Markdown files containing this content, and formattet in a consisten fashion. These files, when imported into any markdown editor (preferably Obsidian), allows the user to analyze on all or parts of the collected information. Obsidian has tools to easily detect correlations between the information, providing a much-needed overview of the collected information.

## How do we intend to use OSINTer?
Our current intent with OSINTer is deploying it internally where needed as to aid CTI team in easily identify relevant sources for future CTI reports, and to deploy a single central instance of OSINTer to start building an archive of historical data.

In the future, it is hovewer also our intend to use OSINTer in conjunction with detection and analysis tools made further down the line. There is currently an effort ongoing to convert the backend of OSINTer from a RDBMS and files on the disk, to an Elasticsearch cluster, which would not only allow extensibility in a way that is currently impossible, potentially allowing for intercommunication between OSINTer instances, and allow for integration of future tools, like Project Grapevine plan proposed by Combitech.


# Quickstart/How-To-Use
*This section has been outdated by the latest updates, and there is work going on to update it*

- Install the ansible package from your repos along with python 3 and the "cryptography" python package.
- Setup a new server using one of the supported distributions listed below and configure a regular user with sudo and SSH access using an SSH key.
  While it is not neccessarily needed to install python 3 on the remote machine, it is recommended, to limit the possibilities of bugs.
- Clone the [OSINTansible](https://gitlab.com/osinter/ansible) git repo and navigate to that directory
- Execute ``` ansible-playbook -K playbooks/main.yml -u [regular_user] -i [remotes] --key-file [private_key_location] ``` with remotes being a comma seperated list of remote servers (add a single trailing comma if only using one remote server), regular_user being the regular, non-root user you set up just before and private_key_location being the path to the private key for your ssh connection.
- When using an SSH key, remember to protect it with ```chmod 400 [private_key_location]```.
- Supply the password for the [regular_user] when asked for the "BECOME password". This will be used for sudo priviledge escalation when needed.
- For distributions with a firewall pre-installed (CentOS and Rocky Linux) remember to open port 80 and 443 on the right interfaces to allow HTTPS and HTTP traffic comming in and out.

## Potential problems
While OSINTer is designed to be installed on a host or series of hosts, which have just been installed, it can also be installed on host(s) running other software. Keep in mind that doing so will probably interfere with the following list of software if it's already installed:

### Nginx
OSINTer utilizes Nginx to utilize the frontend portion of the solution. In order to do so, the webserver will be reconfigured for OSINTer.
- It will replace the nginx config file found at /etc/nginx/nginx.conf??? This will make the nginx service run as the osinter-web user
- It will create a new site in /etc/nginx/site-available and create a symlinkto that in /etc/nginx/sites-enabled
- It will restart the service

### Elasticsearch
OSINTer utilizes Elasticsearch as the main DB for storing collected information, and while the installation of Elasticsearch done by OSINTansible is not system-wide (and therefore won't interfere with the files of any current installation), it will attempt to start Elasticsearch with the default ports (9200 and 9300), which might interfere with already running instances of Elasticsearch, and (due to the high RAM usage) also could get one of the two Elasticsearch proccesses killed

# Supported Systems
Currently, these are the supported distributions using x86_64 architecture:
- Debian 11
- Arch
- Rocky Linux 8

We do recommend running OSINTer on Arch Linux, as this has proven to - for unknown reasons - have a substantial perfomance increase over the other distributions during our very extensive testing, but we do realize that this unfortunatly isn't possible foreveryone, and therefore we fully support the other platforms listed.


# Custom Certificates for the frontend
When installing OSINTer you have the option of providing it with a CA certificate and CA private key, then the ansible installation will write a certificate for your server, which it will utilize for it's webfront. Alternatively OSINTer will generate a selfsigned certificate which will be used instead. The process of using your own CA is as follows:
- Rename a copy of the CA private key to "ca.key" and move it to the "./vars/CA"directory in the OSINTer-ansible folder before installing
- Rename a copy of a certificate signed by the CA to "ca.crt" and move it to that same directory
- Now simply follow the instructions in the quick guide to install OSINTer. The ansible playbooks will automatically recognize the CA and use it for signing the certificates.

# Kibana Dashboards
As OSINTer uses Elasticsearch in the backend for storing data, Kibana can be used to visualize the information scraped by OSINTer. To simplify this proccess, this repo includes a couple of Kibana Dashboards in the KibanaDashboards directory, which (if Kibana has been setup and connected to the same Elasticsearch as OSINTer) can be imported into Kibana using the following command:

``` curl -X POST "[kibana_web_adress]/api/saved_objects/_import?createNewCopies=true" -H "kbn-xsrf: true" --form file=@[dasboard_file_name] ```

Example of how to use command, with Kibana running on localhost, with an elastic user with the password set to "elastic" and using the Articles dashboard:

``` curl -X POST "https://elastic:elastic@localhost:5601/api/saved_objects/_import?createNewCopies=true" -H "kbn-xsrf: true" --form file=@./KibanaDashboards/OSINTerArticles.ndjson```

# In Depth Details
![flowchart](https://gitlab.com/osinter/osinter/raw/master/flowchart.png)

So how does OSINTer function? There is a (admittedly quite primitive and missing a lot of details) flowchart included just above, but if that's not your coup of tea, then here a quick rundown of the inner functions of OSINTer.

## What are profiles?
To understand the script, an understanding of the profiles that enables this script to run in the first place is certainly neccessary. Profiles are in short simply data structured in a JSON format specifying where and what to scrape. These are custom created on a site to site basis, and since nearly all news sites have the same structure (more or less) on all of their articles, they're made to describe some generic rules on where to find given pieces of information on a page, like in what HTML element with what tag the date is to be found, or what element is encapsulating the text in the articles.

## OSINTbackend

*This section has been outdated by the latest updates, and there is work going on to update it*

### Phase 1
Firstly, a scheduler of some sorts starts OSINTbackend. This could be anything from a systemD timer to a simple script set to run at specified intervals, but if deploying OSINTer using the included ansible solution, this scheduler will simply be consisting of a few cronbjobs. Once started, OSINTbackend will gather a list of the profiles within the OSINTprofiles directory and scrape the frontpage/RSS feed of each newssite represented in those profiles for the URL of up to 10 of the newest articles. The limit at 10 hasn't shown to be a problem yet, as OSINTbackend is being run, once an hour, meaning that it never misses articles, but should it be shown to cause problems, it can simply be increased. For now it's mostly there for historical reasons. This proccess results in a dictionary of lists looking something like this:

```
{
	"bleepingcomputer" : ["https://bleepingcomputer.com/news/...", "https://bleepingcomputer.com/news/...", ...],
	"trendmicro" : ["https://blog.trendmicro.com/...", "https://blog.trendmicro.com/...", ...]
	"(newsite nr. n)" : [(article nr. 1 URL), (article nr. 2 URL), ...]
}
```

Once a dictionary of lists of URLs for the newest articles has been obtained, OSINTbackend will go on to do a static scraping of meta information for these articles (using the Python Requests library). This includes the title, description, author, publish date and so on, and while most of the documentation and code for OSINTer refers to this as just OG (Open Graph) tags, some of the information is actually also gathered from other HTML elements like script tags with the type "application/ld+json" (which is oftentimes automatically generated by CMS systems). This information is then collected for all the articles, compiled into a dictionary and then send to two places, 1. into the PostgreSQL DBMS for future retrival and 2. to the second phase of OSINTbackend.

### Phase 2
In the second phase of OSINTbackend, it dynamically scrapes the articles to get the contents of them (using a combination of the Python Selenium framework and the Gecko webdriver for Firefox). The reason scraping the article for a second time, is that while doing the static scraping of webpage is quick and ressource effective (both regarding IO and local ressources), dynamically scraping the webpage gives us a lot more freedom and precission. The internet is a chaotic place that doesn't always follows the relevant guidelines and standards, and dynamically scraping a webpage by emulating a browser doesn't only allow us to bypass systems for preventing spam, and potentially pages that load dynamically using javascript (which is not possible using static scraping), but it also allows us to inject custom javascript into the running browser proccess in between loading the page, and scraping the contents of it, allowing us to do a lot of things like fix broken links and image sources. These small pieces of javascript is saved in the OSINTJSInjections directory in the OSINTbackend project, and can be specified to be used for a specific news site in the profiles.

Then, when the dynamic scraping of articles is done, it's time to sort out the irrelevant parts of the article and only keep the wanted content. This is firstly done by selecting the "container", so to speak, for the article contents (so this is oftentimes a div containing the actual text of the article), and then removing all the unwanted content from this. This way we get a simple way of keeping the parts we want, while sorting out all the unwanted content which often pollutes articles on the modern web. Once the text has been located, this is once again sent to two places; 1. to a markdown converter, which - using the Python [markdownify library](https://github.com/matthewwithanm/python-markdownify) - will convert the HTML elements in the article like tables and img tags to markdown for future storage and 2. to the third phase of OSINTbackend.

### Phase 3

The third phase of OSINTbackend is possibly the most interresting. The two prior steps was simply collecting existing content and selecting the relevant parts of it, but this one is using that data to further enrich the articles before writting them to a markdown file. This is done by proccessing the article contents in 3 different ways to based on that generate some keywords and tags that can be used to easily summarize articles and group them based on key terms, and is done as follows:

1. The first way of generating keywords is the simplest, and is less about actually generating keywords and more about simply extracting objects of interrest in the text. This step uses a dictionary comprissed of regex's to find objects of potential interrest in the article, which could be things like IPv4 and 6 adresses, email adresses and URL's, but also MITRE IDs and CVE numbers. This also means that adding more objects of interrest for OSINTbackend to look for when scraping future articles is as simple as adding a regex to this dictionary.

2. The second uses the specified keywords lists in the OSINTbackend/tools/keywords/ directory, to - based on finding some specific words in the articles - tag the markdown file with the relevant terms, which is refered to as "Manual Tags" in the code (As the blueprints - aka the keyword files - for tagging is created manually in contrast to the next step). Again, adding potential tags for OSINTbackend to use in the feature, is as simple as creating more keyword files (a proccess described in the README of the [OSINTbackend repo](https://gitlab.com/osinter/backend)) and placing those in the keyword files directory.

3. The third and last proccess for tagging the articles tries to extract technical terms and names from the articles and tag the MD files with those. It does this by firstly cleaning the text content of the article, and then comparing every single word in the article to a list of the 370.000 most common words in the english language. If a specific word is found in the article, but not in this dictionary, it seems resonable to assume that this word is some kind of name or technical term, and if it's found enough times in the article text, then the article MD file is tagged with it.

This proccess of generating tags might seem like one that is quite ressource intensive, as it loops over the contents of every article multiple thousand times, but our testing has shown that it increases the time it takes to scrape an article with less than 0.5 seconds on old, low-end hardware, which - given the sometimes up to 10 seconds long time for the simple act of dynamically scraping the article - doesn't seem unreasonable.

Once these 3 phases is done, the data is then collected and using the markdownTemplate.md file in the OSINTbackend/tools directory is all stored in a markdown file named after the title of the article in a directory that follows this naming "OSINTbackend/articles/[newssite name]", and then the article is marked as "scraped" in the database, to mark that the scraping of that specific article is done, and the OSINTwebserver interface can start presenting it to the user.

## OSINTwebserver
Now, OSINTwebserver isn't nearly as complicated as OSINTbackend, but it's certainly still worth quickly touching on, as it is the main way of handling the data gathered by OSINTbackend. OSINTwebserver is, at it's core, as simple flask application, that using OSINTmodules, is able to fetch details about the newest article from the PostgreSQL DBMS and markdown files from the disk and present them to the user.

If you're using the includes OSINTansible to setup OSINTer, OSINTwebserver comes installed as default, available on port 443 with a selfsigned certificate for HTTPS (while self-signed certificates doesn't give the same protections against MITM attacks, it does protect against simple sniffing attacks). It's made accessible using gunicorn as the WSGI server, and utilizing Nginx as a reverse proxy for fast static file access and HTTPS. As OSINTwebserver dynmically generates URLs both for pages and for static content, this also means that by setting the SCRIPT_NAME env variable for gunicorn and using the proxy_pass function in Nginx, it is possible to "submount" OSINTer on a path on a webserver, as to allow that webserver to host other ressources.

### Potential security concerns

We are aware that OSINTwebserver is likely to be solution that is deployed in enviroments where secure applications that doesn't leave servers vulnerable to information leaking and potentially enabling attackers to use them to gain a foothold on the internal networks is absolutetly critical. Therefore security is - along with scalability and ease-of-use - one of the top priorities when developing OSINTer and specifically OSINTwebserver, as this is going to be the front facing software that the user actually interacts with. The following list is some of the things that we have done so far to combat potential missuse of OSINTwebserver:

#### Common web vulnerabilities

- **CSRF**: As all forms is handled by WTForms, an CRSF token is added to all of them, and the backend won't validate the form without this present in the request. All our attempts at either leaking this token, or forging a request with a fake one has failed so far.
- **SQL injection**: All communication to the PostgreSQL DBMS is done using the psycopg2 library to properly sanitize and format all user input which should render this attack type useless. Furthermore, different pieces of the applications uses different users in the DBMS, following the principle of least priviledge, meaning that unless the user found an SQL injection vulnerability in either the login or signup form, they won't be able to leak any sensitive information (which is currently only password hashes).
- **XSS**: No input is taken from the user, stored on disk and the displayed back to the user, which should render this attack impossible. All input actually taken from the user is throughly sanitized and validated before being parsed anywhere in the application to ensure that even other potential vulnerabilities doesn't pop up and nearly all output from OSINTwebserver is rendered using the Jinja2 templating engine which will automatically escape anything problematic.
On interresting attack might be possible hovewer. When reading mode is enabled, OSINTwebserver reads markdown files directly from the disk parses these through a Markdown to HTML converter, and then **bypasses** the escaping of problematic characthers in Jinja2, to put the HTML created from the markdown files directly into the template. This means that given that any of our sources was to post malicious javascript in the articles, and it was able to get through the HTML to Markdown converter and then Markdown to HTML converter, it would in theory be possible to execute XSS attacks on the final enduser. This hovewer was assessed to be highly unlikely, as all of our sources is fairly trusted, and we haven't so far succeeded in getting javascript through the HTML to Markdown converter, as it strips unneeded elements.
- **Open-redirects**: The is_safe_url in the OSINTflask file should be able to reliably verify whether an url is safe or not to redirect the user to. While this hasn't been testet as throughly as the rest of the application, it should be quite robust.

#### Password storage

It is often that we see that even big cooporations having problems with password storage, but luckily modern libraries and technologies have made it a lot easier to do this right. OSINTwebserver uses the Argon2id memory intensive hashing algorithm using the argon-cffi library and api for Python, using the defaults inbuilt in the argon-cffi api as these was deemed sensible and sufficiently secure. Should you want other paramters to further strengthen or possibly weaken it to run it on older hardware (though neither of these should really be needed, unless running this is in a strongly memory-constrained docker container) you can simply change the PasswordHasher object in OSINTwebserver/OSINTmodules/OSINTusers.py, and the password will be rehashed next time the user logs in.

#### Local file permissions

As it is desirable to have the webserver run reliably and persistently (so that it also survives a reboot), our gunicorn instance is being run as a SystemD service. This service is being run as the osinter-web user, setup by the ansible playbook, but as the group http. The reason for this desicion not to run the it using the osinter group instead, is to allow Nginx to access the socket file created the gunicorn instance, as the Nginx config file has been modified to make Nginx run also as the group http. This allows intercommuncation between the to proccesses, without opening our socket file up to the whole system, potentially allowing every proccess on the system to eavsdrop on the communication. Even without those permission setting the eavsdropping scenario is still extremly unlikely to prove to be a problem, as the commincation between Nginx and the gunicorn proccess is also HTTPS, but it does prevent any proccess from writting garbage to the socket, effectivly executing a DOS attack. Furthermore, the right permissions allows to do some manual modifications to run HTTP instead of HTTPS between Nginx and gunicorn, should the HTTPS be a problem regarding solutions like LetsEncrypt.


# Contributers
## People
Thanks to all of these people for assisting in making this project become a reality.<br>
<a href="https://github.com/bertmad3400/"><img src="https://avatars.githubusercontent.com/u/57845632?v=4" width="100" height="100" alt="bertmad3400"/></a>
<a href="https://github.com/TheHangryBadger/"><img src="https://avatars.githubusercontent.com/u/74346591?v=4" width="100" height="100" alt="TheHangryBadger"/></a>
<a href="https://github.com/dtclayton/"><img src="https://avatars.githubusercontent.com/u/46198611?v=4" width="100" height="100" alt="dtclayton"/></a>

## Organisations
Thanks to Combitech A/S for helping with kickstarting the idea and allocating resources for the project development.

<a href="https://www.combitech.com/denmark"><img src="https://www.combitech.com/siteassets/combitech-logo-vitbg.png" width="400"/></a>
