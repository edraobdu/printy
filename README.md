# Printy

![PyPI](https://img.shields.io/pypi/v/printy) ![PyPI - License](https://img.shields.io/pypi/l/printy)

Printy lets you colorize and apply some standard formats to your text with
an intuitive and friendly API based on flags to specify the formats. You can
either apply a global format or inline formats to specific parts of your text!

![Printy Demo](github/printy_demo.gif)


### Installation

you can either clone this repository or install it via pip
```python
pip install printy
```
### How to use it?

Once you install printy, you can find a short but concise documentation about the
available flags and the syntax opening a python console and running the following 
command:
```python
from printy import helpme
```
This will print out some instructions right away.
##### Using global flags

Printy is still a 'print' statement, so you can use it as it is:
```python
printy("Some text")
```
You can use a global set of flags to specify a format you want to apply to the text,
let's say we want to colorize a text with a bold blue and also adding an underline:
```python
printy("Some text", 'bBU')
```
##### Using inline format
Although applying a global format is interesting, it is not as much as applying
some specific format to some section of the text only. For that, printy uses a 
intuitive syntax to accomplish that goal. Use the [] to specify the flags to use
for formatting the text, right before the text, and the @ to finish the formatting 
section:
```python
printy("Still [rI]Some@ Text")
```
The text that is not surrounded by the format syntax will remain with the predefined 
format.

But you can always override this default color for inline format specifying the flags 
in the 'default' parameter
```python
printy("Still [rI]Some@ Text", default="b")
```
Or, you can override the whole format without having to change the inline format:
```python
printy("Still [rI]Some@ Text", "b")
```

### Dependencies

Printy currently support Python 3.5 and up. Printy is currently only tested in 
Unix based operative systems.

### Contributing

Please feel free to contact me if you want to be part of the project and contribute.
We'll looking forward to improve this simple but effective application. 
