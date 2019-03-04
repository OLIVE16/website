# RSS Website Template

This is a basic template for you to use for your team website.


## Modifying the template

You can change the template design as much as you want - in fact we want you to!
This website is pretty boring right now. Use pictures, videos, gifs and stories from your racecar experience
to make this website pop!

There are a couple constraints however. First, your lab reports must remain accessible at these links:


    https:://github.mit.edu/pages/rss2019-[TEAM_NUMBER]/website/labs/[LAB_NUMBER]


Also for the sake of the graders, please make sure that the text remains **black on white**.


And finally don't add too much javascript/bloat.
We're going to need to go through a whole bunch of these websites rapidly
and we don't want it to feel like learning modules.


## Setting up the template

You will be hosting this template using [github pages](https://pages.github.com/).
If you haven't already done so, have your team make an organization on [github.mit.edu](github.mit.edu).
Make sure your organization is named ```rss2019-#``` where "#" is your team number (not your car number!). Do not pad the number with zeros.


Then fork this repo into your organization.
In the settings page of the forked repo scroll down to the "Github Pages" section. Under "Source", click the dropdown menu and select "master branch" then hit save.
You should now be able to see the template if you navigate to:


    https://github.mit.edu/pages/rss2019-[TEAM_NUMBER]/website/


Now in order to modify the template, clone your fork and read on to the next section. 


## Using the template

We've made this template as straightforward as we could to use.
You can edit this using markdown which is the same language the lab reports are written in.
It is very simple and there are plenty of guides online about how to use it.


We've written a small python script that takes your markdown files (named ```README.md```) and turns the into HTML files (named ```index.html```) for the web.
Each markdown file is contained in its own directory and after it is turned into HTML you will be able to view that page at:


    https://github.mit.edu/pages/rss2019-[TEAM_NUMBER]/website/my/directory


Running the python script requires a small library for converting markdown, so first run:


    sudo apt-get install python3-pip
    sudo pip3 install mistune


Then, if for example you wanted to edit your lab 3 report you would do the following:


    # Edit lab 3
    vim website/labs/3/README.md


    # Run the python script to convert to HTML
    ./make.py


    # Stage, commit and push your changes
    git add website/labs/3/README.md website/labs/3/index.html
    git commit -m "Edited lab 3"
    git push origin master


**Note that any edits you make to ```index.html``` files will be overwritten whenever you run ```make.py```**.
Edit the ```README.md``` files if you want to edit text. Edit the ```make.py``` file if you want to edit the generated HTML code.


Edit the variable ```TEAM_NUMBER``` in the ```make.py``` file to edit the displayed team number in the header - this will also make it so the Github link points to the correct page. Also edit the ```VIDEO_LINK``` variable to change where the Video tab links to.


The template also supports $\LaTeX$ via mathjax! For inline math use single dollar signs  and for multiline math use use double dollar signs like this:

$$
\begin{align}
  e^{i\pi} + 1 = 0
\end{align}
$$
