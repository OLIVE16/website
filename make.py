#!/usr/bin/env python3

import os
import mistune

TEAM_NUMBER = "19"
VIDEO_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def parse_readme(directory):
    # Make sure there is a readme file
    readme = os.path.join(root, "README.md")
    if not os.path.isfile(readme):
        return

    path_to_root = os.path.relpath('.', directory)

    # Open an output file
    f = open(os.path.join(directory, "index.html"), 'w+')

    # Write a header
    f.write("<!DOCTYPE HTML><html><head>")
    # Title
    f.write("<title>RSS Team " + TEAM_NUMBER + "</title>")
    # Stylesheet
    f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"")
    f.write(os.path.join(path_to_root, "css/style.css"))
    f.write("\">")
    # Add mathjax
    f.write("<script type=\"text/x-mathjax-config\">")
    f.write("MathJax.Hub.Config({tex2jax: {")
    f.write("inlineMath: [['$','$']],")
    f.write("displayMath: [['$$','$$']],")
    f.write("skipTags: [\"script\",\"noscript\",\"style\",\"textarea\",\"code\"]")
    f.write("},")
    f.write("TeX: {equationNumbers: {autoNumber: \"AMS\"}}});")
    f.write("</script>")
    f.write("<script type=\"text/javascript\" async ")
    f.write("src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML\">")
    f.write("</script>")
    # End Header
    f.write("</head>")

    # Begin the body
    f.write("<body>")
    # Add a bar at the top with the team name
    f.write("<div id=\"main\">")
    f.write("<div id=\"logo\">")
    f.write("<div id=\"logo_text\">")
    f.write("<h1><a href=\"" + path_to_root + "\"><span class=\"logo_colour\">")
    f.write("RSS Team " + str(TEAM_NUMBER))
    f.write("</span></a></h1>")
    f.write("<h2>MIT Spring 2019</h2>")
    f.write("</div></div>")
    # Add a menu bar
    f.write("<div id=\"header\">")
    f.write("<div id=\"menubar\">")
    f.write("<ul id=\"menu\">")
    # Select the write page
    if "labs" in directory:
        lab_class = "selected"
        home_class = ""
    else:
        home_class = "selected"
        lab_class = ""
    f.write("<li class=\"" + home_class + "\"><a href=\"" + path_to_root + "\">Home</a></li>")
    f.write("<li class=\"" + lab_class + "\"><a href=\"" + os.path.join(path_to_root, "labs") + "\">Labs</a></li>")
    f.write("<li><a href=\"" + VIDEO_LINK + "\">Video</a></li>")
    f.write("<li><a href=\"https://github.mit.edu/rss2019-" + str(TEAM_NUMBER) + "\">Github</a></li>")
    f.write("</ul></div></div>")
    f.write("<div id=\"site_content\">")
    f.write("<div id=\"content\">")

    # Add the text from the README
    readme = os.path.join(directory, "README.md")
    with open(readme, 'r') as readme_f:
        renderer = mistune.Renderer(hard_wrap=False,escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        data = readme_f.read()
        f.write(markdown(data))

    # Write the footer
    f.write("</div></div></div>")
    f.write("</body>")
    f.write("</html>")

    # Close the file
    f.close()

if __name__ == "__main__":
    for root, subdirs, files in os.walk("."):
        parse_readme(root)
