#!/usr/bin/python

# Used for interacting with the file system
import os

# Mainly used for sleeping
import time

# Used both for determing paths to a certain file/directory and opening files for quick reading
from pathlib import Path

# For checking if string matches regex
import re

# For filling out the markdown template at last
from string import Template

# For manipulating lists in a way that's less memory intensive
import itertools

# The profiles mapping the different websites are in json format
import json

# Used to gather the urls from the articles, by reading a RSS feed
import feedparser

# Used for scraping static pages
import requests

# Used for dynamically scraping pages that aren't static
from selenium import webdriver

# Used for running the browser headlessly
from selenium.webdriver.firefox.options import Options

# For parsing html
from bs4 import BeautifulSoup

# For generating random numbers for scrambling the article overview
import random

# For converting html to markdown
from markdownify import markdownify

# For counting and finding the most frequently used words when generating tag
from collections import Counter

# Used for normalising cleartext from articles
import unicodedata

def checkIfURL(URL):
    if re.match(r"https?:\/\/.*\..*", URL):
        return True
    else:
        return False

# Function for intellegently adding the domain to a relative path on website depending on if the domain is already there
def catURL(rootURL, relativePath):
    if checkIfURL(relativePath):
        return relativePath
    else:
        return rootURL[:-1] + relativePath

# Function for taking an arbitrary string and convert it into one that can safely be used as a filename and for removing spaces as those can be a headache to deal with
def fileSafeString(unsafeString):
    allowedCharacthers = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    unsafeString = unsafeString.replace(" ", "-")
    safeString = ''.join(c for c in unsafeString if c in allowedCharacthers)
    return safeString


# Function for using the class of a container along with the element type and class of desired html tag (stored in the contentDetails variable) to extract that specific tag. Data is found under the "scraping" class in the profiles.
def locateContent(contentDetails, soup, multiple=False):

    content = list()

    # Getting the html tag that surrounds that tag we are interrested in
    contentContainer = soup.find(class_=contentDetails['containerClass'])

    try:
        # We only want the first entry for some things like date and author, but for the text, which is often split up into different <p> tags we want to return all of them
        if multiple:
            return contentContainer.find_all(contentDetails['element'].split(';'), class_=contentDetails['class'])
        else:
            return contentContainer.find(contentDetails['element'], class_=contentDetails['class'])
    except:
        return BeautifulSoup("Unknown", "html.parser")

# Function for reading all profile files and returning the content in a list if given no argument, or for returning the contents of one profile if given an argument
def getProfiles(profileName=""):
    # Listing all the profiles by getting the OS indepentent path to profiles folder and listing files in it
    profileFiles = os.listdir(path=Path("./profiles"))

    if profileName == "":
        # List for holding the information from all the files, so they only have to be read one
        profiles = list()

        # Reading all the different profile files and storing the contents in just created list
        for profile in profileFiles:

            # Stripping any potential trailing or leading newlines
            profiles.append(Path("./profiles/" + profile).read_text().strip())

        return profiles
    else:
        return Path("./profiles/" + profileName + ".profile").read_text().strip()

def RSSArticleURLs(RSSURL, profileName):
    # Parse the whole RSS feed
    RSSFeed = feedparser.parse(RSSURL)

    # List for holding the urls from the RSS feed
    articleURLs = [profileName]

    # Extracting the urls only, as these are the only relevant information. Also only take the first 10, if more is given to only get the newest articles
    for entry in itertools.islice(RSSFeed.entries, 10):
        articleURLs.append(entry.id)

    return articleURLs

# Scraping targets is element and class of element in which the target url is stored, and the profileName is prepended on the list, to be able to find the profile again when it's needed for scraping
def scrapeArticleURLs(rootURL, frontPageURL, scrapingTargets, profileName):

    # List for holding the urls for the articles
    articleURLs = [profileName]

    # The raw source of the site
    frontPage = requests.get(frontPageURL)

    # Parsing the source code from the site to a soup
    frontPageSoup = BeautifulSoup(frontPage.content, 'html.parser')

    # Some websites doesn't have a uniqe class for the links to the articles. If that's the case, we have to extract the elements around the link and the extract the link from those
    if scrapingTargets['linkClass'] == "":
        # Looping through the first 10 of the elements that in the profile has been specified by element type and class to contain the links we want. Only first 10 due to same reason in RSSArticleURLs
        for linkContainer in itertools.islice(frontPageSoup.find_all(scrapingTargets['element'], class_=scrapingTargets['class']), 10):

            # The URL specified in the source will ofc be without the domain and http information, so that get's prepended here too by removing the last / from the url since the path also contains one
            articleURLs.append(catURL(rootURL, linkContainer.find('a').get('href')))

    # Others do hovewer have a uniqe class for the links, and here we can just extract those
    else:
        for link in itertools.islice(frontPageSoup.find_all('a', class_=scrapingTargets['linkClass']), 10):
            articleURLs.append(catURL(rootURL, link.get('href')))

    return(articleURLs)


def scrapePageDynamic(pageURL, loadTime=3, headless=True):

    # Setting the options for running the browser driver headlessly so it doesn't pop up when running the script
    driverOptions = Options()
    driverOptions.headless = headless

    # Setup the webdriver with options
    driver = webdriver.Firefox(options=driverOptions)

    # Actually scraping the page
    driver.get(pageURL)

    # Sleeping a pre-specified time to let the driver actually render the page properly
    time.sleep(loadTime)

    # Getting the source code for the page
    pageSource = driver.page_source

    driver.quit()

    return pageSource


def gatherArticleURLs(profiles):

    articleURLs = list()

    for profile in profiles:

        # Parsing the json properly
        profile = json.loads(profile)['source']

        # For those were the RSS feed is useful, that will be used
        if profile['retrivalMethod'] == "rss":
            articleURLs.append(RSSArticleURLs(profile['newsPath'], profile['profileName']))

        # For basically everything else scraping will be used
        elif profile['retrivalMethod'] == "scraping":
            articleURLs.append(scrapeArticleURLs(profile['address'], profile['newsPath'], profile['scrapingTargets'], profile['profileName']))

    return articleURLs

# Function for scraping OG tag from page
def scrapeOGTags(URL):
    pageSource = requests.get(URL)
    if pageSource.status_code != 200:
        print("Error: Status code " + str(pageSource.status_code) + ", skipping URL: " + URL)
        return []
    pageSoup = BeautifulSoup(pageSource.content, 'html.parser')

    OGTags = list()

    for tag in ["og:title", "og:description", "og:image"]:
        OGTags.append(pageSoup.find("meta", property=tag).get('content'))

    return OGTags

# Function used for ordering the OG tags into a dictionary based on source, that can then be used later
def collectOGTags(profileName, URLList):

    # Gets the name of the news media
    siteName = json.loads(getProfiles(profileName))['source']['name']

    # Creating the data structure that will store the OG tags
    OGTagCollection = {}
    OGTagCollection[profileName] = []

    # Looping through each URL for the articles, scraping the OG tags for those articles and then adding them to the final data structure
    for URL in URLList:
        OGTags = scrapeOGTags(URL)
        if OGTags != []:
            # If the sitename isn't in the title, it will be added now
            if siteName.lower() not in OGTags[0].lower():
                OGTags[0] += " | " + siteName

            # The og tag details will then be written to the final data structure
            OGTagCollection[profileName].append({
                'source'        : profileName,
                'url'           : URL,
                'title'         : OGTags[0],
                'description'   : OGTags[1],
                'image'         : OGTags[2]
            })

    return OGTagCollection

# Function used for scrambling the OG tags. The reason the URLs isn't simply scrambled before scrapping the OG tags and thereby making the proccess of scramblin them a lot simpler, is that this will scramble the source, but the newest articles will still be first.
def scrambleOGTags(OGTagCollection):
    # The list of the scrambled OG tags that will be returned
    scrambledTags = list()

    while OGTagCollection != {}:
        # Choosing a random source (eg. bleepingcomputer or zdnet or something else)
        randomSource = random.choice(" ".join(OGTagCollection).split())

        # Moves the newest article from a random source from the ordered list to the scrambled
        scrambledTags.append(OGTagCollection[randomSource].pop(0))

        # Checks if individual list is empty and removing it if it is
        if OGTagCollection[randomSource] == []:
            del OGTagCollection[randomSource]

    return(scrambledTags)

# Function used for constructing the CSS and HTML needed for the front end used for presenting the users with the different articles
def constructArticleOverview(OGTags):
    HTML = ""
    CSS = ""
    for i,article in enumerate(OGTags):
        HTML += '<article id="card-' + str(i) + '"><a href="' + article['url'] + '"><h1>' + article['title'] + '</h1></a></article>\n'
        CSS += '#card-' + str(i) + '::before { background-image: url(' + article['image'] + ');}\n'


    # Make template for HTML file
    contentList = {
        'CSS': CSS,
        'HTML': HTML
    }

    # Open the template for the HTML file
    with open(Path("./webFront/index.html"), "r") as source:
        # Read the template file
        sourceTemplate = Template(source.read())
        # Load the template but fill in the values from contentList
        filledTemplate = sourceTemplate.substitute(contentList)
        # Write the filled template to a new file that can then be opened
        with open(Path("./webFront/overview.html"), "w") as newHTMLFile:
            newHTMLFile.write(filledTemplate)

# Function for collecting all the small details from the article (title, subtitle, date and author)
def extractArticleDetails(contentDetails, soup):
    details = list()
    for detail in contentDetails:
        if contentDetails[detail] != "":
            details.append(locateContent(contentDetails[detail], soup).get_text())
        else:
            details.append("Unknown")

    return details

def extractArticleContent(textDetails, soup, clearText=False, delimiter='\n'):
    # Get the list with the <p> tags in it
    textList = locateContent(textDetails, soup, True)

    if textList == "Unknown":
        raise Exception("Wasn't able to fetch the text for the following soup:" + str(soup))

    assembledText = ""

    # Loop through all the <p> tags, extract the text and add them to string with newline in between
    for element in textList:
        if clearText:
            assembledText = assembledText + element.get_text() + delimiter
        else:
            assembledText = assembledText + str(element) + delimiter

    return assembledText

# Function for scraping everything of relevans in an article
def scrapeArticle(currentProfile, articleURL):

    # Scraping the full source code for the article and parsing it to a soup
    articleSource = scrapePageDynamic(articleURL)
    articleSoup = BeautifulSoup(articleSource, 'html.parser')

    articleDetails =    extractArticleDetails(currentProfile['scraping']['details'], articleSoup)
    articleContent =    extractArticleContent(currentProfile['scraping']['content'], articleSoup)
    articleClearText =  extractArticleContent(currentProfile['scraping']['content'], articleSoup, True)

    return articleDetails, articleContent, articleClearText

# Function for taking in text from article (or basically any source) and outputting a list of words cleaned for punctuation, sole numbers, double spaces and other things so that it can be used for text analyssis
def cleanText(clearText):
    # Normalizing the text, to remove weird characthers that sometimes pop up in webarticles
    cleanClearText = unicodedata.normalize("NFKD", clearText)
    # Removing all contractions and "'s" created in english by descriping possession
    cleanClearText = re.sub(r'\'\S*', '', cleanClearText)
    # Remove all characthers that isn't spaces, numbers or letters
    cleanClearText = re.sub(r'[^\w\s-]', ' ', cleanClearText)
    # Remove those words that are only numbers
    cleanClearText = re.sub(r'\s\d*\s', ' ', cleanClearText)
    # Remove line endings
    cleanClearText = re.sub(r'\n', ' ', cleanClearText)
    # Making sure there isn't anywhere with more than one consecutive space
    cleanClearText = re.sub(r'\s\s', ' ', cleanClearText)

    # Converting the cleaned cleartext to a list
    clearTextList = cleanClearText.split(" ")

    return clearTextList

# Function for taking in a list of words, and generating tags based on that. Does this by finding the words that doesn't appear in a wordlist (which means they probably have some technical relevans) and then sort them by how often they're used. The input should be cleaned with cleanText
def generateTags(clearTextList):

    # List containing words that doesn't exist in the wordlist
    uncommonWords = list()

    # Generating set of all words in the wordlist
    wordlist = set(line.strip() for line in open("./wordlist.txt", "r"))

    # Find all the words that doesn't exist in the normal english dictionary (since those are the names and special words that we want to use as tags)
    for word in clearTextList:
        if word.lower() not in wordlist and word != "":
            uncommonWords.append(word)

    # Take the newly found words, sort by them by frequency and take the 10 most used
    sortedByFreq = [word for word in Counter(uncommonWords).most_common(10)]

    # only use those who have 3 mentions or more
    tagList = list()
    for wordCount in sortedByFreq:
        if wordCount[1] > 2:
            tagList.append(wordCount[0])

    return tagList



def createMDFile(sourceName, sourceURL, articleDetails, articleContent, articleTags):

    # Define the title
    title = articleDetails[0]

    # Define the subtitle too, if it exist
    if articleDetails[1] != "Unknown":
        subtitle = articleDetails[1]
    else:
        subtitle = ""

    # Convert the link for the article to markdown format
    MDSourceURL = "[article](" + sourceURL + ")"

    # Define the details section by creating markdown list with "+"
    MDDetails = ""
    detailLabels = ["Source: ", "Link: ", "Date: ", "Author: "]
    for i,detail in enumerate([sourceName, MDSourceURL, articleDetails[2], articleDetails[3]]):
        MDDetails += "+ " + detailLabels[i] + detail + '\n'

    # Convert the scraped article to markdown
    MDContent = markdownify(articleContent)

    # And lastly, some tags (TODO)
    MDTags = "[[" + "]] [[".join(articleTags) + "]] [[" + sourceName + "]]"

    # Creating a structure for the template
    contentList = {
        'title': title,
        'subtitle': subtitle,
        'information': MDDetails,
        'articleContent': MDContent,
        'tags': MDTags
    }

    # Converting the title of the article to a string that can be used as filename and then opening the file in append mode (will create file if it doesn't exist)
    MDFileName = fileSafeString(articleDetails[0]) + ".md"

    with open(Path("./markdownTemplate.md"), "r") as source:
        sourceTemplate = Template(source.read())
        filledTemplate = sourceTemplate.substitute(contentList)
        with open(Path("./" + MDFileName), "w") as newMDFile:
            newMDFile.write(filledTemplate)

    # Returning the file name, so it possible to open it in obsidian using an URI
    return MDFileName

# Function for moving the newly created markdown file into the obsidian vault, and opening it in obsidian
def openInObsidian(vaultName, vaultPath, fileName):
    # Firstly, move the file to the vault
    os.rename(Path(fileName).resolve(), Path(vaultPath + fileName))

    # Then encode vault and filename for url and remove the .md file extension from the file at the same time
    encVaultName = requests.utils.quote(vaultName, safe='')
    encFileName = requests.utils.quote(fileName[:-3], safe='')

    # Construct the URI for opening obsidian:
    URI = "obsidian://open?vault=" + encVaultName + "&file=" + encFileName

    # And lastly open the file in obsidian by using an URI
    driver = webdriver.Firefox()
    driver.get(URI)

def handleSingleArticle(vaultName, vaultPath, profileName, articleURL):

    # Load the profile for the article
    currentProfile = json.loads(getProfiles(profileName))

    # Gather the needed information from the article
    articleDetails, articleContent, articleClearText = scrapeArticle(currentProfile, articleURL)

    # Generate the tags
    articleTags = generateTags(cleanText(articleClearText))

    # Create the markdown file
    MDFileName = createMDFile(currentProfile['source']['name'], articleURL, articleDetails, articleContent, articleTags)
    openInObsidian(vaultName, vaultPath, MDFileName)

# Function for scraping the the news front side, gather a lot of urls for articles and then present them in an overview
def getSpecificArticle():
    articleURLLists = gatherArticleURLs(getProfiles())

    OGTagCollection = {}
    for URLList in articleURLLists:
        # Getting the name of the current profile, which is stored in the start of each of the lists with URLs for the different news sites
        currentProfile = URLList.pop(0)
        # Getting the relevant part of the dictionary created by collectOGTags
        OGTagCollection[currentProfile] = collectOGTags(currentProfile, URLList)[currentProfile]

    # Constructing the article overview HTML file
    constructArticleOverview(scrambleOGTags(OGTagCollection))

# Dump function for just downloading all the articles the program can scrape
def downloadBulk():
    articleURLLists = gatherArticleURLs(getProfiles())

    for URLlist in articleURLLists:
        currentProfile = URLlist.pop(0)
        for url in URLlist:
            handleSingleArticle("Testing", "/home/bertmad/Obsidian/Testing/", currentProfile, url)
