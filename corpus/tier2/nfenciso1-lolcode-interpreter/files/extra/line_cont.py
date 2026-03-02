import re

content = 'HAI\n\tI HAS A var ...\n\tITZ ...\n55\n\tVISIBLE var\nKTHXBYE'
newContent = ''
rxLineCont = r"(\".*\.\.\..*\")|([ \t]\.\.\.[ \t\n]*)|([\w\W \t\n])"



results = re.findall(rxLineCont, content)
for i in results:
    if (i[1]):
        newContent += " "
    elif (i[0]):
        newContent += i[0]
    elif (i[2]):
        newContent += i[2]

print(content)
# print(results)
print(newContent)