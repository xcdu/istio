# Note
## Node Summary
Based on the summary, we found the following direct child nodes of the 'article' node:
```plain
* p
* h3
* h4
* table
* ul
* h5
* figure
* pre
* code
* div
* nav
* section
* ol
```

In detail, we found 
```plain
* div
* ul
* p
```
in the direct children node of index page.

And we found
```plain
* section
* figure
* h3
* nav
* div
* ul
* p
* pre
* h4
* h2
* h5
* code
* table
* ol
```
in the direct children node of introduction page.

## How to handle various kinds of nodes

As to index page, we can slice the contents of article nodes by "div", "ol" and 
"ul".

As to introduction page, we can firstly slice the contents of article nodes by 
headline nodes, such as "h2", "h3", "h4", and "h5", as the sub-level.

Then, slice the contents of the sub-level by "div", "section", "ul", "ol", 
"table", "figure", and "pre".

Note that, we recognize contents of "code", "p", "li", "a" as content text.

Specially, we get two different kinds of codes in Istio Doc (inline and code 
blocks). We should check the class attribute first to confirm whether it is the 
inline code.





## How to Distinguish Index and Introduction Pages
```python
has_section_index = selector.xpath("boolean(//*[@class='section-index'])")
```

## Proper Command Line & Template
### Command Line
'code' node with 'command-output' class
### Template
'code' node with 'language-yaml' class
