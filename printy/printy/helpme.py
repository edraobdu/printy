
helpme = """
#########################################################
#########################################################

[bBU]PRINTY@

Printy lets you colorize and apply some standard formats to your text with
an intuitive and friendly API based on flags to specify the formats. You can
either apply a global format or inline formats to specific parts of your text!

[nB]Let's get started!@

[B]COLORS@

[gH]#### Gray Scale@
[k]'k' -> Applies a black color to the text@
[g]'g' -> Applies a grey color to the text@
[w]'w' -> Applies a white color to the text@

[rH]#### Red Scale@
[<r]'<r' -> Applies a darkred color to the text@
[r]'r'  -> Applies a red color to the text@
[r>]'r>' -> Applies a lightred color to the text@

[nH]#### Green Scale@
[<n]'<n' -> Applies a darkgreen color to the text@
[n]'n'  -> Applies a green color to the text@
[n>]'n>' -> Applies a lightgreen color to the text@

[yH]#### Yellow Scale@
[<y]'<y' -> Applies a darkyellow color to the text@
[y]'y'  -> Applies a yellow color to the text@
[y>]'y>' -> Applies a lightyellow color to the text@

[bH]#### Blue Scale@
[<b]'<b' -> Applies a darkblue color to the text@
[b]'b'  -> Applies a blue color to the text@
[b>]'b>' -> Applies a lightblue color to the text@

[mH]#### Magenta Scale@
[<m]'<m' -> Applies a darkmagenta color to the text@
[m]'m'  -> Applies a magenta color to the text@
[m>]'m>' -> Applies a lightmagenta color to the text@

[cH]#### Cyan Scale@
[<c]'<c' -> Applies a darkcyan color to the text@
[c]'c'  -> Applies a cyan color to the text@
[c>]'c>' -> Applies a lightcyan color to the text@

[oH]#### Orange Scale@
[<o]'<o' -> Applies a darkorange color to the text@
[o]'o'  -> Applies a orange color to the text@
[o>]'o>' -> Applies a lightorange color to the text@

[pH]#### Purple Scale@
[<p]'<p' -> Applies a darkpurple color to the text@
[p]'p'  -> Applies a purple color to the text@
[p>]'p>' -> Applies a lightpurple color to the text@

[B]FORMATS@

[B]'B' -> Applies a bold font weight to the text@
[U]'U' -> Applies an underline to the text@
[I]'I' -> Applies an italic font type to the text@
[H]'H' -> Highlights the text@
[S]'S' -> crosses out the text, aka Strike@
[D]'S' -> Dim effect@


[B]HOW TO USE IT?@

First import printy:

[n]    >>>@ [<o]from@ printy [<o]import@ printy

Now apply one or more of the available flags to the text like this:

[n]    >>>@ printy([n>]'Some text to be formatted'@[<o],@ [n>]'b'@)
    [b]Some text to be formatted@

[n]    >>>@ printy([n>]'Some text to be formatted'@[<o],@ [n>]'bHI'@)
    [bHI]Some text to be formatted@

Or as Inline format, use the \[\] to specify the flags, and the \@ to finish
the format for a specific section:

[n]    >>>@ printy([n>]'\[r\]Red\@ Default Color \[yH\]Yellow Highlighted\@ Default Color'@)
    [r]Red@ Default Color [yH]Yellow Highlighted@ Default Color

You can always override the whole format with a global flag:

[n]    >>>@ printy([n>]'\[r\]Red\@ Default Color \[yH\]Yellow Highlighted\@ Default Color'@[<o],@ [n>]'b'@)
    [b]Red Default Color Yellow Highlighted Default Color@

Or you can change only the predefined color:

[n]    >>>@ printy([n>]'\[r\]Red\@ Default Color \[yH\]Yellow Highlighted\@ Default Color'@[<o],@ [r]predefined@=[n>]'b'@)
    [r]Red@ [b]Default Color@ [yH]Yellow Highlighted@ [b]Default Color@

[n]    >>>@ printy([n>]'\[r\]Red\@ Default Color \[yH\]Yellow Highlighted\@ Default Color'@[<o],@ [r]predefined@=[n>]'nBIU'@)
    [r]Red@ [nBIU]Default Color@ [yH]Yellow Highlighted@ [nBIU]Default Color@

If you need to use one of the special characters ('\[', '\]', '\@'), simply escape them

[n]    >>>@ printy([n>]'\[B\]\\\[myemail\\\@mydomain.com\\\]\@'@)
    [B]\[myemail\@mydomain.com\]@

Now you can do stuffs like:

[n]    >>>@ text = [n>]'Hello world, python is awesome!!!'@
[n]    >>>@ printy(text.replace([n>]'python'@[<o],@ [n>]'\[r\]python\@'@))
    Hello world, [r]python@ is awesome

Or some html highlighting:

[n]    >>>@ html = (
[n]    ...@ [n>]'<div \[p\]class=\@\[n>\]"active"\@ \[p\]id=\@\[n>\]"my-div"\@>'@
[n]    ...@ [n>]'    <span \[p\]data-some-data=\@\[n>\]"extra-data"\@>\[p\]Some text\@</span>'@
[n]    ...@ [n>]'</div>'@)
[n]    >>>@ printy(html[<o],@ [r]default@=[n>]'y>'@)
    [y>]<div@ class=[n>]'active'@ id=[n>]'my-div'@[y>]>@
        [y>]<span@ data-some-data=[n>]'extra-data'@[y>]>@Some text[y>]</span>@
    [y>]</div>@

Or, you can use it with python's formatting strings as well:

[n]    >>>@ minutes = [c>]60@
[n]    >>>@ printy([n>]f'A day has \[y\]@[<o]{@minutes * [c>]24@[<o]}@[n>]\@ minutes'@)
    A day has [y]1400@ minutes

[B]What about @[p>B]input@()?

printy comes with a wrapper for the python built-in [p>]input@() function

[n]    >>>@ [<o]from@ printy [<o]import@ inputy

Try adding adding some formats the same way you did with printy and 
[y]Check this link for a full documentation!@

https://github.com/edraobdu/printy    
"""

