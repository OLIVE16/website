#!/usr/bin/env python3

import os
import mistune

def parse_readme(directory):
    # Make sure there is a readme file
    readme = os.path.join(root, "README.md")
    if not os.path.isfile(readme):
        return

    path_to_root = os.path.relpath('.', directory)

    # Open an output file
    f = open(os.path.join(directory, "contents.html"), 'w+')

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
    # Add the text from the README
    readme = os.path.join(directory, "README.md")
    with open(readme, 'r') as readme_f:
        renderer = mistune.Renderer(hard_wrap=False,escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        data = readme_f.read()
        f.write(markdown(data))

    # Close the file
    f.close()

if __name__ == "__main__":
    for root, subdirs, files in os.walk("."):
        parse_readme(root)
