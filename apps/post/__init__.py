import re

def scan_picture_url(content):
    result = ""
    match_object = re.match(".*\s+src=\"(.*)\"", content)
    if match_object != None:
        matches = match_object.groups()
        result = matches[0]
    return result

def html_to_text(html):
    #p = re.compile(r'<.*?>')
    #return p.sub('', html)
    result = re.sub('<.*?>', '', html)
    result = re.sub("&.+?;", "", result)
    return result

