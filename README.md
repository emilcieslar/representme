# REPRESENT ME
University of Glasgow ITECH team project


## INSTALLATION GUIDE (assuming you have unix based command line):

1. **Open up command line**
2. **Clone the project to your directory**

   `git clone https://github.com/emilcieslar/tangowithdjango.git`
   
3. **Go to the tangowithdjango/tangowithdjango folder**

   `cd tangowithdjango/tangowithdjango/`

4. **Install requirements.txt to your new virtual environment** 
   
   If you don't know how to use virtual environments, refer to this url: [tangowithdjango](http://www.tangowithdjango.com/book17/chapters/requirements.html#virtual-environments)

   `pip install -r requirements.txt`
   
5. **Make migrations on representME and apply them** 
   
   `python manage.py makemigrations representME`

   `python manage.py migrate`

6. **Run Populate/Populate_from scraper.py in order to create some data (this is gonna take a little while [few minutes])**

   `python Populate/Populate_from\ scraper.py`
   
   **However, if you are on unix based system, you will get errors therefore follow this simple fix:**
   
   Copy Populate_from scaper.py to the base directory
        
   `cp Populate/Populate_from\ scraper.py Populate_from\ scraper.py`
        
   As well as data.py
        
   `cp Populate/data.py data.py`
        
   Then run Populate_from scraper.py from your base directory
        
   `python Populate_from\ scraper.py`
   
7. **You are good to go!**

   `python manage.py runserver`
   
   And open up your browser with address http://127.0.0.1/representME/
