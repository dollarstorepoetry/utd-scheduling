"""
Displays the information associated with a UT Dallas course code.
"""
# import datetime
import requests
import tkinter as tk  # for work on a gui after 10 nov

global course_code

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
    clean_html = raw_html
    emp = clean_html.find("<")
    while (emp != -1):
        fin = clean_html.find(">")  # this should theoretically work since this is finding the FIRST instance every time
        clean_html = clean_html[:emp] + clean_html[fin+1:]
        emp = clean_html.find("<")
    return clean_html


def format(desc, textwidth):
    """
    Formats a program as to be readable on a box with width textwidth.
    """
    # add new lines to make things more convenient
    

    # loop through all the words; add a new line before a word if
    # the length of the line exceeds textwidth
    words = desc.split()
    pass


def old_main():
    """
    Old version of main() method that works in terminal.
    """
    course_code = input("Enter the name of your class (space between school and number): ")
    catalog_url = build_url(course_code)
    try:
        catalog_request = requests.get(catalog_url)
        course_info = parse(catalog_request.text)
        print(course_info)
    finally:
        input("hit enter or any key or whatever to terminate")


def main():
    # metadata; <head>
    root = tk.Tk()
    root.geometry("500x550")
    root.title("UTD Catalog Search")

    # not meta stuff
    def go_through_the_motions(cc):
        # don't know if I should keep this as an inner method, but I also don't see why it shouldn't be
        CourseInfoDisp.delete("1.0", tk.END)
        CourseInfoDisp.insert(tk.END, "Getting course info from catalog.utdallas.edu...")  # this doesn't display for some reason
        course_code = cc
        course_info = parse(requests.get(build_url(cc)).text)  # all of the old main method in one line of code because i am a thug
        
        CourseInfoDisp.delete("1.0", tk.END)
        CourseInfoDisp.insert(tk.END, course_info)
    
    l1 = tk.Label(root, text="Enter the name of your class (space between school and number): ")
    l1.pack()
    e = tk.Entry(root)
    e.pack()
    button = tk.Button(root, text="Get Class Info", width = 10, command=lambda: go_through_the_motions(e.get()))
    button.pack()
    root.bind("<Return>", lambda event:go_through_the_motions(e.get()))  # binds enter to do the same thing as button
    CourseInfoDisp = tk.Text(root, width = 50)
    CourseInfoDisp.pack()
    termbutt = tk.Button(root, text="Quit",width=10, command=root.destroy)
    termbutt.pack()
    root.bind("<Escape>", lambda event:root.quit)
    # Label to show status of program
    root.mainloop()


if __name__ == '__main__':
    main()
