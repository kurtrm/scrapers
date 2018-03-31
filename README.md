#Web Scrapers

This repository contains various web scrapers I've made. Each uses requests or Beautiful Soup, or selenium.

##Transcript Transcriber
I wasn't able to retrieve the HTML using either Selenium or requests since UF uses
SAML2.0 authentication, which uses a lot of redirection. I downloaded the HTML and parsed it from a file.
This script is rather unorganized and could use some refactoring.

Additionally, the page itself had scattered text that wasn't contained in any HTML elements. I opted
to settle for a 90% solution.

##PCT Completion Rates
This was the easier scraper to build, as the data was pretty rigidly structured.
I had to use Selenium because the year selector was controlled by Javascript. This script
is more compartmentalized and can be run from the command line.

It also puts all the data into MongoDB.