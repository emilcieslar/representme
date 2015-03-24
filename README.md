# REPRESENT ME
University of Glasgow ITECH team project


INSTALLATION GUIDE (assuming you have unix based command line):

1. Open up command line
2. Clone the project to your directory 

   `git clone https://github.com/emilcieslar/tangowithdjango.git`
   
3. Install requirements.txt to your virtual environment 
   
   If you don't know how to use virtual environments, refer to this url: [tangowithdjango](http://www.tangowithdjango.com/book17/chapters/requirements.html#virtual-environments)

   `pip install -r requirements.txt`
   
4. Make migrations on representME and apply them 
   
   `python manage.py makemigrations representME`

5. Run Populate_from scraper.py in order to create some data

   `python Populate_from scraper.py`
   
6. You are good to go
