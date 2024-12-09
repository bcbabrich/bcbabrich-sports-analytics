from bs4 import BeautifulSoup

html_doc = """
 <html>
  <head>
   <title>
    The Dormouse's story
   </title>
  </head>
  <body>
   <div class="sister" href="http://example.com/elsie" id="link1">
    <div>div1a</div>
    <div>div1b</div>
   </div>
   <div class="sister" href="http://example.com/lacie" id="link2">
    <div>div2a</div>
    <div>div2b</div>
    <div>div2c</div>
   </div>
   <div class="sister" href="http://example.com/tillie" id="link3">
    <div>div3a</div>
   </div>
  </body>
 </html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')
print('....')
print(soup.prettify())
print('....')
print(soup.body.contents)
print('....')
new_contents = [x for x in soup.body.contents if x != '\n']
print(len(new_contents))
