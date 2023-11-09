"""
Displays the information associated with a UT Dallas course code.
"""
import datetime
import requests

def build_url(code) -> str:
    """
    Builds the URL for a course given the course code.
    """
    ourl = "https://catalog.utdallas.edu/"
    ourl += f"{datetime.date.today().year}/"
    thing = code.split(" ")
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
    unparsed_div = gross_raw_html[begin:end]

    # clean up the div so it's actually meaningful
    # two options:
    #   1. get rid of the html tags entirely, or
    #   2. somehow integrate the link function of those pages into the program

    # this is an implementation of option 1
    # loop through unparsed_div string and just delete html tags
    # i = 0
    # while (i < len(unparsed_div)):
    #     if unparsed_div[i] == "<":

    # use find() to delete all html tags
    emp = unparsed_div.find("<")
    while (emp != -1):
        fin = unparsed_div.find(">")  # this should theoretically work since this is finding the FIRST instance every time
        unparsed_div = unparsed_div[:emp] + unparsed_div[fin+1:]
        emp = unparsed_div.find("<")

    return unparsed_div



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
