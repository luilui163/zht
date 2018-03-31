
## Links
<http://someurl>  

<someone@example.com>  


[like this](http://www.google.com)  


## Reference Links

You can also put the [link URL][1] below the current paragraph
like [this][2].  

    [1]:http://url  
    [2]:http://another.url 'A funky title'


Or you can use a [shortcut][] reference,which
links the text "shortcut" to the link named
"[shortcut]" on the next paragraph.

[shortcut]:http://goes//with/the/name/text

## Artifact Links
### Simple Links
Most commonly,the artifact identifier can simply
be surrounded with square brackets.  

[MyWikiPage]    #Wiki - name of wiki page  
[#123]    #Tracker - ticket number

### Two-part Links
[bugs:#1]  
[features:#1]  

### Three-part Links

## Basic Text formatting
Use `*` or `_` to emphasize things:
*this is a italic` and _so is this_  
**this is in bold** and __so is this__  
***this is bold and italic*** and ____so is this___  

<s>this is strike through text</s>  

### BLockquotes
Use the > character in front of the line.
>Use it if you'are quoting a person,a song or whatever

### Preformatted Text
If you want some text to show up exactly as you write it,without Markdown
doing anything to it,just indent every line by at least 4 spaces (or 1 tab)

    This line won't *have any markdown* formatting applied.
    I can even write <b>HTML</b> and it will show up as text.

## Lists
* an asterisk `*` starts an unordered list
+ or you can also use the `+` character

To start an ordered list,write this:  
1. this starts a list *with* numbers
+ this will show as number "2"
* this will show as number "3"
9. any number,+,- or * will keep the list going.
    * just indent by 4 spaces (or tab) to make a sub-list  
        1. keep indenting for more sub lists
    * here I'm back to the second level
## Tables
| First Header | Second Header |
| ------------ | ------------- |
| content cell | content cell  |
| content cell | content cell  |

You can use markdown syntax with table cells for formatting  

## Horizontal Rule
Just put three or more `*`s or `-`s on a line
***

---


## Images
![altenate text](https://sourceforege.net/icon_linux.gif)  

You can also use a title if you want,like this:  
![tiny arrow](https:/sourceforge.net/images/icon_linux.gif "tiny arrow")  

To references an attached image,just use the img macro.You can add more attributes:  
[[img src=attached-image.jpg alt=foobar]]  

## Videos
[[embed url=http://www.youtube.com/watch?v=6YbBmqUnoQM]]

## Escapes and HTML
use `\` to escape special characters.  

## Table of Contents

    [TOC]  

    # section 1  
    ## sub-section 1  
    # section 2  


## Code Highlighting
The language will be detected automatically,if possible.Or you can specify it.  
:::python
import pandas as pd  


~~~html
<a href="#">my code</a>
~~~

```html
<a href="#">My code</a>
```

## Includes
You can embed another wiki page directly:  
[[include ref=SamplePage]] 

 No example output is available for this code because it only works on real
 wiki pages.Try it in your wiki!  

 Also,you can embed a file directly from a repository:  
 [[include repo=code path=README]]  

 [[include repo=p:myproject:code path/ew/forms.py]]  

## Neighborhood Blog posts
## Project blog posts

## download button
[[donwload_button]]  

## Gittip button
[[gittip_button username=foo]]  

## Project Member list  
[[members]]

## Project Screenshots
You can show all the screenshots for current project as thumbnails 
that are linked to the full-size image.  
[[project_screenshots]]
















