"""
Displays the information associated with a UT Dallas course code.
"""
# import datetime
import requests
import tkinter  # for work on a gui after 10 nov

# 10 nov commit changes (delete before committing):
# created remove_html_tags() method
# simplified build_url()
# changed a few comments and variable names to be more descriptive
# https://dev.to/casualcoders/git-beginner-crash-course-3ggk or just use the built in vsc stuff lol


def build_url(course_code) -> str:
    """
    Builds the URL for a course given the course code.
    """
    ourl = "https://catalog.utdallas.edu/"
    # ourl += f"{datetime.date.today().year}/"
    ourl += "now/" # not quite sure if this will work 100% of the time, but this should be a thing UTD does
    thing = course_code.split(" ")
    if int(thing[1][0]) > 4:
        ourl += "graduate/"
    else:
        ourl += "undergraduate/"
    ourl += f"courses/{thing[0].lower()}{thing[1]}"
    return ourl


def parse(gross_raw_html, div_id="bukku-page") -> str:
    """
    Returns the information of the course in readable format.
    The id for the div that contains all the information seems to consistently be called
    "bukku page", and is thus the default value for the div_id.
    """

    # find the course information div using the "given" (default value) div id
    div_tag = f'<div id="{div_id}">'
    begin = gross_raw_html.find(div_tag)
    end = begin + gross_raw_html[begin:].find("</div>")  # end is expressed this way because it starts with begin at 0
    div = gross_raw_html[begin:end]

    # clean up the div so it's actually meaningful
    # two options:
    #   1. get rid of the html tags entirely, or
    #   2. somehow integrate the link function of those pages into the program (future future ambitions)

    # this is an implementation of option 1
    div = remove_html_tags(div)

    return div


def remove_html_tags(raw_html) -> str:
    """
    Removes all HTML tags (info between <angle brackets>) from a block of HTML.
    Intended to be used with sections of text... don't know why you would use it otherwise lol
    """
    # use find() to delete all html tags

    # print(raw_html,"\n\n")
    emp = raw_html.find("<")
    while (emp != -1):
        fin = raw_html.find(">")  # this should theoretically work since this is finding the FIRST instance every time
        raw_html = raw_html[:emp] + raw_html[fin+1:]
        emp = raw_html.find("<")
    return raw_html


def main():
    course_code = input("Enter the name of your class (space between school and number): ")
    catalog_url = build_url(course_code)
    try:
        catalog_request = requests.get(catalog_url)
        course_info = parse(catalog_request.text)
        print(course_info)
    finally:
        input("hit enter or any key or whatever to terminate")


if __name__ == '__main__':
    main()
