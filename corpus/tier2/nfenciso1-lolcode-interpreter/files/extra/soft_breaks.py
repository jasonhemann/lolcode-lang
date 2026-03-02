import re

content = 'HAI\nI HAS A str OBTW this,\n\tis a multiline, commentTLDR\n\tI HAS A var,55\n\tBTW this,is a comment\n\t"Hello, World!"\nKTHXBYE'
newContent = ''
rxSoftBreak = r"(\".*,.*\")|([ \t\n]BTW.*)|([ \t\n]OBTW[\w\W]*?TLDR)|(,)|([\w\W \t\n])"



results = re.findall(rxSoftBreak, content)
for i in results:
    if (i[3]):
        newContent += "\n"
    elif (i[0]):
        newContent += i[0]
    elif (i[4]):
        newContent += i[4]

print(content)
print(results)
print(newContent)