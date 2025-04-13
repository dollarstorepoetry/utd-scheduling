"""
Displays the course description associated with a UT Dallas course code.
"""
# import datetime
import requests
import tkinter as tk
import sys

course = ""

def build_url(course_code) -> str:
    """
    Builds the URL for a course given the course code.
    """
    #
    # implement some error handling here later lol
    #
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
    
    Not the most extensible of methods but that's fine maybe
    """
    clean_html = raw_html
    emp = clean_html.find("<")
    while (emp != -1):
        fin = clean_html.find(">")  # this should theoretically work since this is finding the FIRST instance every time

        # it's formatting time
        tag_type = clean_html[emp:fin+1]
        if tag_type == '</h1>' or tag_type == '</span>':  # do new line
            clean_html = clean_html[:emp] + "\n" + clean_html[fin+1:].strip()
        else:
            clean_html = clean_html[:emp] + clean_html[fin+1:]
        emp = clean_html.find("<")
    return clean_html


def newline_format(text_block, textwidth):
    """
    Formats a block of text to be readable on a box with width textwidth.

    this is probably like a really stupid method and tkinter probably alread
    has some stuff built in that does this but like. do i care¿ no
    """
    descarr = text_block.split("\n") # split the text block by new line. we're gonna edit this in place bc why would we not

    # format each section (delimited by \n) of the block of text individually
    for i in range(len(descarr)):
        sectionarr = descarr[i].split(" ")  # split *this* block by whitespace
        secstr = ""

        # loop through each word within the block and do the nice new line formatting thing
        line_length = 0
        for j, word in enumerate(sectionarr):
            # once the length of the line exceeds textwidth,
            # start a new line
            if (line_length+len(word) >= textwidth):
                sectionarr[j-1] += '\n'  # start new line
                # sectionarr[j] = sectionarr[j].strip()  # take weird spaces off
                line_length = 0  # mathematically start new line
            line_length += len(word) + 1  # +1 to account for spaces!

        for thing in sectionarr:  # do u like my variable names :3
            secstr += (thing + " ") if (thing[-1] != "\n") else (thing)
            # >complains about readability >uses ternary operator >mfw
        descarr[i] = secstr

    newarrstr = ""  # oh nooo i didn't declare the variable at the beginning of the block 🤓
    for section in descarr:
        newarrstr += section + "\n"
    return newarrstr


def old_main(course_code=0):
    """
    Old version of main() method that works entirely in terminal.
    """
    if course_code == 0:
        print("just force an error (e.g. feed something other than a course code, pass a signal e.g. ctrl+c) to exit i'm soooo lazy")
        course_code = input("\nEnter the course code associated with your class: ")
    try:
        catalog_url = build_url(course_code)
        catalog_request = requests.get(catalog_url)
        course_info = parse(catalog_request.text)
        print(course_info)
        print()
    except:
        print("error encountered. exiting")


def ambatukinter():
    # metadata; <head>
    root = tk.Tk()
    root.geometry("500x500")
    root.title("UTD Catalog Search")
    textwidth = 50

    # not meta stuff
    def go_through_the_motions(cc):
        # don't know if I should keep this as an inner method, 
        # but I also don't see why it shouldn't be
        CourseInfoDisp.delete("1.0", tk.END)
        CourseInfoDisp.insert(tk.END, "Getting course info from catalog.utdallas.edu... (this is secretly an error message. bug wip)")  
        # this doesn't display for some reason
        course_code = cc
        catalog_url = build_url(course_code)
        course_info = parse(requests.get(catalog_url).text)
        course_info = newline_format(course_info, textwidth) 
        
        CourseInfoDisp.delete("1.0", tk.END)
        CourseInfoDisp.insert(tk.END, course_info)
    
    l1 = tk.Label(root, text="Enter the course code of your class: ")
    l1.pack()
    e = tk.Entry(root, width=9)
    e.pack()

    button = tk.Button(root, text="Get Class Info", width = 10, command=lambda: go_through_the_motions(e.get()))
    button.pack()
    root.bind("<Return>", lambda event:go_through_the_motions(e.get()))  

    CourseInfoDisp = tk.Text(root, width = textwidth)
    CourseInfoDisp.pack()
    termbutt = tk.Button(root, text="Quit",width=10, command=root.destroy)
    termbutt.pack()
    root.bind("<Escape>", lambda event:root.quit)
    # Label to show status of program
    root.mainloop()


def main():
    if len(sys.argv) == 1:
        old_main()
        return
    elif len(sys.argv) < 2:
        raise ValueError("Please indicate whether to run the CLI or the GUI.")
    
    choice = sys.argv[1]
    if (choice.upper() == 'CLI'):
        while True:
            old_main()
    elif (choice.upper() == 'GUI'):
        ambatukinter()
    else: 
        old_main(choice)



if __name__ == '__main__':
    main()
