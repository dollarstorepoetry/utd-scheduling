"""
Displays the course description associated with a UT Dallas course code.
"""
# import datetime
import requests
import tkinter as tk

course = ""

def build_url(course_code) -> str:
    """
    Builds the URL for a course given the course code.
    """

    # implement some error handling here later lol

    ourl = "https://catalog.utdallas.edu/"
    # ourl += f"{datetime.date.today().year}/"
    ourl += "now/" # not quite sure if this will work 100% of the time, but this should be a thing UTD does

    global course
    course = course_code.split(" ")
    if (len(course) == 1):  # split if no space is given
        # once the first int is reached, make the thing into the format that we like
        for i, ch in enumerate(course_code):
            if ch.isdigit():
                course = [course_code[:i], course_code[i:]]
                break


    if int(course[1][0]) > 4:
        ourl += "graduate/"
    else:
        ourl += "undergraduate/"
    ourl += f"courses/{course[0].lower()}{course[1]}"
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


# def format(desc, textwidth):
#     """
#     Formats a program as to be readable on a box with width textwidth.
#     please don't integrate this into code right now it does NOT work
#     """
#     # add new lines to make things more convenient
#     thing = desc.split(" ")
#     do_a_break = False
#     wi = 1  # skip the first word because it's the course code with no space between school and number
#     while (not do_a_break):
#         word = thing[wi]
#         if type(word[0]) != int:
#             for ci, ch in enumerate(word):
#                 if (type[ch] == int): # this doesn't work
#                     desc = desc[:ci] + "\n" + desc[ci:]  # this doesn't work
#                     break
#         wi += 1

#     # add a new line before prereqs

#     # loop through all the words; add a new line before a word if
#     # the length of the line exceeds textwidth
#     lensum = 0
#     for wi, word in enumerate(thing):
#         lensum += len(word)
#     pass


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
        CourseInfoDisp.insert(tk.END, "Getting course info from catalog.utdallas.edu... (this is secretly an error message. bug wip)")  # this doesn't display for some reason
        course_code = cc
        course_info = parse(requests.get(build_url(course_code)).text)  # all of the old main method in one line of code because i am a thug
        
        CourseInfoDisp.delete("1.0", tk.END)
        CourseInfoDisp.insert(tk.END, course_info)
    
    l1 = tk.Label(root, text="Enter the name of your class (space between school and number): ")
    l1.pack()
    e = tk.Entry(root, width=9)
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
    # doink = """MATH3351 - Advanced CalculusMATH 3351 Advanced Calculus (3 semester credit hours) The course covers the interplay of linear algebra, higher dimensional calculus, and geometry. Topics include vectors, coordinate systems, the elementary topology of Euclidean spaces and surfaces, the derivative as a linear map, the gradient, multivariate optimization, vector fields, vector differential operators, multiple integrals, General Stokes Theorem, and differential forms. Applications are given to geometry, science, and engineering. Basic topological intuition is developed. Prerequisites: (A grade of at least a C- in either MATH 2415 or MATH 2419 or equivalent) and a grade of at least a C- in MATH 2418 or equivalent. (3-0) S"""
    # print(format(doink, 0))