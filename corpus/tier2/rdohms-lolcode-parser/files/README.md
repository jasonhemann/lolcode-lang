# DMS LOLCode Parser

This is a LOLCode parser based on previous work by TetraBoy and MailChimp.
It has support for a few more features and may get an overhaul for composer support and modern PHP, just cause.

## Usage

`php bin/lolcode.php <file>`

or 

`php bin/lolcode.php -d <file>`

To enable debug and see generated code.

## Examples

We've packaged up some example scripts in the ./examples/ directory. Here's what they do:
test.lol - This is from Tetraboy's original index.lol example. It opens a SQLite db and prints data from it 
test2.lol - This example shows creating an associative array and printing its values. 
test3.lol - This example shows reading in LOL format, eval'ing it, and then iterating over and printing the 'imported' variables. 
test4.lol - This example shows off using the IO package to download a LOL formatted data file over the intertubes, evals it, and works with the data in the local scope 
test5.lol - This example shows off using the IO package to prompt for input to save in a variable, then spits it back out. 
test6.lol - This is from Tetraboy's original index.lol example. It shows defining a function, variable assignments, and incrememting numbers
raffler.lol - This shows a simple raffler that picks a random name from a file.
