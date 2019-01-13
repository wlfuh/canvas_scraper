import json
import requests
import urllib2
import os

with open('token.txt') as file:
    token = file.read().strip()


base_url = "https://canvas.instructure.com"
headers = {"Authorization" : "Bearer "+token}
data = requests.get("{}/api/v1/courses/".format(base_url), headers=headers, params={"per_page" : 100, "enrollment_state":"active"})
# print(data.text)
courses = json.loads(data.text)
# print(courses)

for course in courses:
    loc = os.path.join('downloaded_pdfs', course["course_code"])
    if not os.path.exists(loc):
        os.mkdir(loc)
    endpoint = "/api/v1/courses/{}/files".format(course["id"])
    data = requests.get(base_url + endpoint, headers=headers, params={"per_page" : 100})
    files = json.loads(data.text)
    #print files
    #print json.dumps(files, indent=4, sort_keys=True)
    for file in files:
        other_filename, extension = os.path.splitext(file["filename"])
        filename = file["display_name"]
        if not filename.endswith(extension):
            filename += extension
        if os.path.exists(os.path.join(loc, filename)):
            continue
        endpoint = "/api/v1/files/{}/public_url".format(file["id"])
        data = requests.get(base_url + endpoint, headers=headers)
        dat = json.loads(data.text)
        if "public_url" in dat:
            pub_url = dat['public_url']
        else:
            continue
        file_data = urllib2.urlopen(pub_url)
        with open(os.path.join(loc, filename),'w+') as f:
            f.write(file_data.read())
        print "Downloaded {} located in {}".format(filename, loc)


# endpoint = "/api/v1/courses/17700000000167212/folders"
# headers = {"Authorization" : "Bearer "+token}
# data = requests.get(base_url + endpoint, headers=headers)
# files = json.loads(data.text)
# print json.dumps(files, indent=4, sort_keys=True)
