## PromoBot

**© 2019 Ursu Stefan-Alin All Rights Reserved**



&nbsp; &nbsp; &nbsp; This was the project I created in order to get the Professional Skills Certificate.
    
&nbsp; &nbsp; &nbsp; This is a web scrapper with whom you can search for limited sales in specific websites. The search process use
informations given by the user such as category or keywords, maximum price and number of pages that will be scrapped.

&nbsp; &nbsp; &nbsp; Also, the project have a complex algorithm who can help the user to avoid fake sales: in a database, the program save
every product scrapped from an website, alongside his price. If the same product, from the same website, will be found
in the future at a higher price, the newly created HTML file will contain a message saying that the same product was found
at a lower price in a certain date.

&nbsp; &nbsp; &nbsp; **Some features might not work if it's not updated. (some HTML tags might need to be changed)**
    
&nbsp; &nbsp; &nbsp; PromoBot.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the main program
        
&nbsp; &nbsp; &nbsp; Documentatie.odt:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the documentation about this project (why I chose it, statistics, what I used, how to use the program, pieces
        of code, etc.)
        
&nbsp; &nbsp; &nbsp; config.cfg:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - a config file
        
&nbsp; &nbsp; &nbsp; scripts/scrappers/*:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the script with whom the program is scrapping a certain website
        
&nbsp; &nbsp; &nbsp; scripts/db.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the script used to communicate with the database
        
&nbsp; &nbsp; &nbsp; scripts/debug.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the script used to create and write in the log file
        
&nbsp; &nbsp; &nbsp; scripts/htmlcreator.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the script used to create the HTML files using informations scrapped from websites
        
&nbsp; &nbsp; &nbsp; scripts/json.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - a class with whom you can read json files
        
&nbsp; &nbsp; &nbsp; scripts/scrapper.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - the class used for scrapping websites
        
&nbsp; &nbsp; &nbsp; scripts/utils.py:
    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - some functions that are used often while the program is running
        
