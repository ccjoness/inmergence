from bs4 import BeautifulSoup
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pz = 'C:\\projects\\inmergence_app\\templates\\PDX_Code_Guild\\CisnerosSandra-Eleven.zip'

with open(pz.replace('zip', 'html'), 'r+', encoding="utf8") as html:
    with open(pz[:-4] + '-rendered.html', 'a', encoding="utf8") as wrt:
        wrt.write('{% extends "base.html" %}')
        wrt.write('{% block content %}')
        for line in html.readlines()[37:-2]:
            wrt.write(line)
        wrt.write('{% endblock %}')

# output = re.sub(r'(.*<body bgcolor="#A0A0A0" vlink="blue" link="blue">)',
#                 string='{% extends "base.html" %}\n{% block content %}\n',
#                 repl="\s"
#                 )
# out_str = ",".join(output)
# with open("output.txt", "w") as outp:
#     outp.write(out_str)
# m = re.search(r'<h1>Title</h1>.*?<h1>', open(pz.replace('zip', 'html'), 'r+', encoding="utf8"), re.DOTALL)
# s = m.start()
# e = m.end() - len('<h1>')
# target_html = html[s:e]
# soup = BeautifulSoup(html, "html.parser")

# html = ""
# for tag in soup.find("body").next_siblings:
#     if tag.name == "body":
#         break
#     else:
#         html += tag
#
# print(html)