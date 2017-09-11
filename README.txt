This is a program to create a local host website that allows for users to login and work with assets.

Disclaimer for potential employers:  This program was created on a weekly basis without knowing what the next week would entail while I was learning, ie. there is a lot of unnecessary code.  Was created on a VM with certain things preinstalled, may not run on other computers.


Export:
	contains files used to export my database data into csv files, also has a few test files.

Import:
	contains files used to import csv file data into the database.

sql:
	contains files to create tables in the database.

src:
	contains files for the interactive website, and connection to the database.

testdoc:
	contains my test plan and test plan results.

preflight.sh:
	runs sql to create tables and imports data into the database if desired.

install_daemons.sh:
	If not run on a server that has apache and postgress downloaded, this should do so.  
	Outdated with the rest of the project, so it is not called with preflight.sh
