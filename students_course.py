import json
import requests

with open('token.txt') as file:
    token = file.read().strip()



base_url = "https://canvas.instructure.com"
headers = {"Authorization" : "Bearer "+token}
data = requests.get("{}/api/v1/courses/".format(base_url), headers=headers, params={"per_page" : 200, "enrollment_state":"active"})
courses = json.loads(data.text)
def get_students(course_id):
    link = "{}/api/v1/courses/{}/users".format(base_url, course_id)
    r = requests.get(link, headers=headers, params={"per_page" : 100, "enrollment_type":"student"})
    res = json.loads(r.text)
    while "next" in r.links and not r.links["next"]["url"] == r.links["first"]["url"]:
        r = requests.get(r.links["next"]["url"], headers=headers, params={"per_page" : 100, "enrollment_type":"student"})
        res += json.loads(r.text)
    return res
students = {
    course["course_code"]:#course["id"]
        set([
            student["name"]
            for student in get_students(course["id"])
            ])
    for course in courses
    }
# print students
def get_intersect(arr):
    intersect = students[arr[0]]
    for i in xrange(1, len(arr)):
        intersect = intersect.intersection(students[arr[i]])
    if intersect:
        print "{} Students in {}".format(len(intersect), " and ".join(arr))
        for s in sorted(intersect):
            print s
        print ""

def combinations_helper(arr):
    if not arr:
        return
    get_intersect(arr)
    old = arr.pop()
    combinations_helper(arr)
    arr.append(old)

def combinations(arr):
    combinations_helper(arr)
    for i in xrange(1, len(arr)):
        last = arr[0]
        for j in xrange(1, len(arr)):
            arr[j - 1] = arr[j]
        arr[-1] = last
        combinations_helper(arr[:-1])

course_names = students.keys()

combinations(course_names)
