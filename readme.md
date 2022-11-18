

# Preety Link

Preety Link is a clone of <a href="https://b1.fileshub.cfd/">FilesHub</a> and <a href="https://enon.eu.org/">Enon.eu.org</a>. Preety Link is a web based tool from where you can generate page to download file by share multiple server link build in flask (Python).


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8](https://img.shields.io/badge/Python-v3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Flask v2.2.2](https://img.shields.io/badge/Flask-v2.2.2-yellowgreen)](https://pypi.org/project/Flask/)

[![AGPL License](https://img.shields.io/badge/JQuery-v3.6.1-orange)](https://jquery.com/download/)




# Setting And Customisation
### Site Configuration
In [config.json](https://github.com/NonSenseHacker/preety-link/config.json) update Website name, Site description, Author name, Site secret key, Admin ID and Password. Don't forget to update database credentials.

### Create Databse
```sql
CREATE TABLE `multi_link` (
  `id` int(11) NOT NULL,
  `file_url` varchar(10) NOT NULL,
  `Date` date NOT NULL,
  `file_name` text NOT NULL,
  `file_ext` text NOT NULL,
  `file_size` int(11) NOT NULL,
  `size_ext` text NOT NULL,
  `Server_1` varchar(255) DEFAULT NULL,
  `Server_2` varchar(255) DEFAULT NULL,
  `Server_3` varchar(255) DEFAULT NULL,
  `Server_4` varchar(255) DEFAULT NULL,
  `Server_5` varchar(255) DEFAULT NULL
);
```
# Deployment
### [Read Documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/)


