# GENIE-Flask-Backend

### To create a new requirements.txt file - 
```pip freeze > requirements.txt``` 

### To setup locally - 
Run - 
<ol>
    <li>pip install -r requirements.txt</li>
    <li>.venv\Scripts\activate</li>
    <li>pymon app.py</li>
    <li>**If pymon keeps on restarting the server, then use -> python app.py</li>
</ol>


### Todo
<ul>
    <li>Write a check to see if a url exists for a keyword or not, can be simply done by checking whether the soup contains the title {keyword} Internships or Total Internships</li>
    <li>Add text cleaner from raser repository to clean resume and job data</li>
    <li>Add ML Model</li>
    <li>Add API calls</li>
    <li>Remove hard coded values for keywords</li>
    <li>Push user data to mongodb collection</li>
    <li>to check for max pages check in soup if 1/3 or 2/3 exists at the bottom of the page</li>
</ul>