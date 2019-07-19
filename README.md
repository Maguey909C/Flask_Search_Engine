# Flask_Search_Engine
Author: Chase Renick

### Introduction
One of the most common challenges for data scientists is determining what data is reliable, what it means, and where to find it within a database, datawarehouse, log file or server.  Large companies which have significant resources often have teams dedicated to data governance that should be managing a company data dictionary, changes within that data, what is being collected and from where, among other things.  However, it is more often the case that little attention is paid to data governance, or worse the importance of how much time is wasted (which translates into money) when employees cannot find the data resources they need or cannot determine what it means. 

Any data scientist who has worked in the industry will validate this point. 

What everyone wants is sometype of searchable data dictionary within their company so that they don't have to ask their peers (or worse superiors) what something means.  Problem is that in order to get a product from a vendor it is usually $$$.

### Project:
This flask search engine is a simple solution to solving this problem. It operates like a normal search engine and has the ability to connect to a backend database that will allow you to edit, delete, create new tables to read from.  

The app can search based on an exact column name contained within a table, or it can search free form text for your underlying idea and generate a list of possible columns that approximate what you are looking for.  It approximates using a weighted score derived from definitions from the columns within your table as well as the column names themselves.  The score can be tweaked based on your needs, but the idea is that it is not simply using string matching to make a connection.  That would be too simple.

This app could be hosted on an instance or internal server for a department or team to use when peforming their projects.  There are lots of places to go from here.

### Conclusion:
We successfully deployed a POC version of this within a company I worked for, and many employees found it very useful.  Hope you do too!
