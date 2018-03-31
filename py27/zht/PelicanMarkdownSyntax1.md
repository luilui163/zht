*[ABBR]: Abbreviation definition

Abbreviated Text: ABBR

Auto link: <http://example.com>

Inline `code`

Bold Italic Text: ***bold italic***, **_bold italic_** and ***normal text

Bold: **bold**, ***bold italic***, **_bold italic_**, and **normal text

Escaped Character: \* \_ \` \& \[ \] \< \> \! \# \\ \" \' \. \- \( \) \{ \} \: \| \~

Explicit Link : [Example](http://example.com)

Footnote Reference[^1]

Italic Text: *italic*, _italic_ and this one is not *italic

Image: ![My image](http://www.foo.bar/image.png)

Inline HTML: <b>bold</b> &nbsp; &#10; &#x0a;

Hard Break Spaces: at end of line  
    that has a continuation.

Mail Link: <me@example.com>

Smart Characters: ... -- --- a's b's. . .

Smart quotes 'this is a quote' "this is a quote"

Strikethrough: ~~strikethrough **strikethrough bold** *strikethrough italic* _strikethrough italic_ ***strikethrough bold italic*** **_strikethrough bold italic_**~~

Subscript: ~subscript~

Superscript ^superscript^

Underline/Inserted: ++underline++

WikiLink: [[Link address and Link Text]]  Creole syntax: [[Link address|Link text]]  [[Link address#anchor|Link text]] GitHub syntax: [[Link text|Link address]] [[Link text|Link address#anchor]]

<!-- Comment -->

> block quote

* bullet list
1. List Item 1
* [ ] task item
* [x] task item (done)
* [X] task item (done)

[^1]: Footnote text

[Reference]: http://example.com#anchor-reference  "Title"
Reference link: [link text][reference] [reference].
Reference image: ![alt text][reference] ![reference].


Term 1
:   Definition 1.1
:   Definition 1.2

Term 2
:   Definition 2.2

| Header Row 1 Cell 1 | Header Row 1 Cell 2 |
| Header Row 2 Cell 1 | Header Row 2 Cell 2 |
| Header Row 2 Cell 1 | Header Row 2 Cell 2 |
|:--------------------|:-------------------:|
| Row 1 Cell 1        |    Row 1 Cell 2     |
| Row 2 Cell 1        |    Row 2 Cell 2     |
| Row 2 Cell 1        |    Row 2 Cell 2     |
[Table Caption]

```language
   Verbatim Block
```

# First level title

First level title
=================

## Second level title

Second level title
------------------

### Third level title

#### Fourth level title

##### Fifth level title

###### Sixth level title

* * *

<div>
Block
</div>



Test Markdown document
======================

Text
----

Here is a paragraph with bold text. **This is some bold text.** Here is a
paragraph with bold text. __This is also some bold text.__

Here is another one with italic text. *This is some italic text.* Here is
another one with italic text. _This is some italic text._

Here is another one with struckout text. ~~This is some struckout text.~~


Links
-----

Autolink: <http://example.com>

Link: [Example](http://example.com)

Reference style [link][1].

[1]: http://example.com  "Example"


Images
------

Image: ![My image](http://www.foo.bar/image.png)

Headers
-------

# First level title
## Second level title
### Third level title
#### Fourth level title
##### Fifth level title
###### Sixth level title

### Title with [link](http://localhost)
### Title with ![image](http://localhost)

Code
----

```
This
  is
    code
      fence
```

Inline `code span in a` paragraph.

This is a code block:

    /**
     * Sorts the specified array into ascending numerical order.
     *
     * <p>Implementation note: The sorting algorithm is a Dual-Pivot Quicksort
     * by Vladimir Yaroslavskiy, Jon Bentley, and Joshua Bloch. This algorithm
     * offers O(n log(n)) performance on many data sets that cause other
     * quicksorts to degrade to quadratic performance, and is typically
     * faster than traditional (one-pivot) Quicksort implementations.
     *
     * @param a the array to be sorted
     */
    public static void sort(byte[] a) {
        DualPivotQuicksort.sort(a);
    }

Quotes
------

> This is the first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.


> A list within a blockquote:
>
> *	asterisk 1
> *	asterisk 2
> *	asterisk 3


> Formatting within a blockquote:
>
> ### header
> Link: [Example](http://example.com)



Html
-------

This is inline <span>html</html>.
And this is an html block.

<table>
  <tr>
    <th>Column 1</th>
    <th>Column 2</th>
  </tr>
  <tr>
    <td>Row 1 Cell 1</td>
    <td>Row 1 Cell 2</td>
  </tr>
  <tr>
    <td>Row 2 Cell 1</td>
    <td>Row 2 Cell 2</td>
  </tr>
</table>

Horizontal rules
----------------

---

___


***


Lists
-----

Unordered list:

*	asterisk 1
*	asterisk 2
*	asterisk 3


Ordered list:

1.	First
2.	Second
3.	Third


Mixed:

1. First
2. Second:
	* Fee
	* Fie
	* Foe
3. Third


Tables:

| Header 1 | Header 2 |
| -------- | -------- |
| Data 1   | Data 2   |