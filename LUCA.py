#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
    This file is part of LUCA.

    LUCA - LEGO Universe Creation (Lab) Archiver
    Created 2013 Brickever <http://systemonbrick.wordpress.com/>

    LUCA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    LUCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with LUCA If not, see <http://www.gnu.org/licenses/>.
"""
import os
import time
import imghdr
import requests
from bs4 import BeautifulSoup

app = "LUCA"
majver = "1.0"
minver = ".2"

# ------------ Begin Illegal Character Check ------------ #


def charCheck(text, folders=False):
    """Checks for illegal characters in text"""
    # List of illegal characters for filenames
    illegal_chars = ["\\", "/", ":", "*", "?", '"', "'", "<", ">", "|"]

    if folders:
        illegal_chars.append(".")
    found_chars = []

    # Get the length of the text, minus one for proper indexing
    len_of_text = len(text) - 1

    # Assign variable containing result of check; default to False
    illa = False

    # -1 so the first character is caught too
    while len_of_text != -1:

        # This character is allowed
        if text[len_of_text] not in illegal_chars:
            # The check goes in reverse, checking the last character first.
            len_of_text -= 1

        # This character is not allowed
        elif text[len_of_text] in illegal_chars:
            # Change value of variable; kill the loop, as we only need
            # to find one illegal character to end the (ball) game.
            illa = True
            found_chars.append(text[len_of_text])
            len_of_text -= 1

    # A(n) illegal character(s) was found
    if illa:
        for char in found_chars:
            # Replace it (them) with a space
            text = text.replace(char, "-")
    del found_chars[:]
    return text

# ------------ End Illegal Character Check ------------ #

# ------------ Begin Username Searches ------------ #


def searchUser(username, take2=False):
    """Find a username on the Creation Lab"""
    if take2:
        # Backup search method for finding the username on the Creation Lab
        url = "http://universe.lego.com/en-us/community/creationlab/displaycreationlist.aspx?SearchText={0}&show=48&page=1".format(
            username)
    else:
        # Search the username on the Creation Lab
        url = "http://universe.lego.com/en-us/community/creationlab/displaycreationlist.aspx?SearchText={0}&order=oldest&show=48&page=1".format(
            username)

    # Get search page content
    r = requests.get(url).content
    soup = BeautifulSoup(r)

    # Holding pen for possible Creations by the user
    creations = []

    # Gather the creations from the page
    for link in soup.find_all('a'):
        if link.get('href')[0:49] == "/en-us/Community/CreationLab/DisplayCreation.aspx":
            creations.append('http://universe.lego.com{0}'.format(
                link.get('href')))

    if not creations:
        # No Creations were found on first search
        if not take2:
            searchUser(username, take2=True)

        # No Creations was found, close LUCA
        print('The username "{0}" was not found on the Creation Lab.'.format(
            username))
        input("\nPress Enter to close LUCA.")
        raise SystemExit(0)

    num_of_creations = len(creations) - 1
    names = []

    # Get the usernames from all Creations from the search
    while num_of_creations != -1:
        r = requests.get(creations[num_of_creations]).content
        soup = BeautifulSoup(r)
        onlineUserName = soup.find(
            id="ctl00_ContentPlaceHolderUniverse_HyperLinkUsername")
        names.append(onlineUserName)
        num_of_creations -= 1

    # These are the first search results
    if not take2:
        memberid = checkUser(username, names, take2=False)
        del creations[:]
        del names[:]
        return memberid

    # These are the second search results
    elif take2:
        memberid = checkUser(username, names, take2=True)
        del creations[:]
        del names[:]
        main(True, memberid=memberid, localUserName=username)
        #return memberid

# ------------ End Username Searches ------------ #


# ------------ Begin Username Checks ------------ #

def checkUser(locuser, webusers, take2=False):
    """Checks if this is the proper username"""
    # Get the proper index of all the names to check
    num_of_names = len(webusers) - 1
    found_name = True

    while num_of_names > -1:
        # The username entered was found
        # begin downloading the creations
        if locuser.lower() == webusers[num_of_names].string.lower():
            memberid = webusers[num_of_names].get('href')[63:99]
            return memberid

        # That username did not match, try next one
        else:
            num_of_names -= 1
            found_name = False

    # We are using the first search results
    if not take2:
        # Search again, using a different query
        if not found_name:
            searchUser(locuser, take2=True)

    # We are using the second query results
    if take2:
        # The username could not be found
        if not found_name:
            print('The username "{0}" does not appear to match with any usernames online.'
                  .format(locuser))
            input("\nPress Enter to close LUCA.")
            raise SystemExit(0)

# ------------ End Username Checks ------------ #


# ------------ Begin Page Number Gathering and Text --> Binary ------------ #


def pageme(soup):
    """Get the number of pages the Creations are on"""
    # Find area containing number of pages
    num_of_pages = soup.find("p", class_="column-navigation").get_text()

    # Remove unneeded text: part 1
    num_of_pages = num_of_pages.replace('''\r
\t\t\t\t\t\t\r\n\t\t\t\t\t\t»\nShow:\n\n12\n24\n36\n48\n\nOrder:
\nMost Recent\nOldest\nRating\n\n''', "")

    # Remove unneeded text: part 2
    num_of_pages = num_of_pages.replace('''\r
\t\t\t\t\t\t\xad\r
\t\t\t\t\t\t«\r
\t\t\t\t\t\t\t\r
\t\t\t\t\t\t''', "")

    # Remove unneeded text: part 3
    num_of_pages = num_of_pages.replace("\r\n\t\t\t\t\t\t\r\n\n", "")
    num_of_pages = num_of_pages.replace("1 of ", "")

    # Convert the number to an integer
    num_of_pages = int(num_of_pages)
    return num_of_pages


def byteme(text):
    """Convert text to binary"""
    bin_text = str.encode(text, encoding="utf-8", errors="strict")
    return bin_text

# ------------ End Page Number Gathering and Text --> Binary ------------ #


def main(userfound=False, memberid=False, localUserName=False):
    """Main LUCA Process"""
    if not userfound:
        localUserName = input("\nEnter your Creation Lab Username: ")
        print('Searching the Creation Lab for user "{0}"'.format(
              localUserName))

        # Search for the username on the Creation Lab
        memberid = searchUser(localUserName, take2=False)

    print("\nYour Creations are now downloading, {0}.".format(
        localUserName))
    print("NOTE: This may take a while.\n")

    # Create folder to save files in,
    # unless it already exists
    if not os.path.exists(localUserName):
        os.mkdir(localUserName)

    # ------------ Begin Creation Gathering ------------ #

    # List of Creations
    creations = []
    num_of_creation_files = 0

    user_url = "http://universe.lego.com/en-us/community/creationlab/displaycreationlist.aspx?memberid={0}&show=48&page=1".format(memberid)
    user_r = requests.get(user_url).content
    user_soup = BeautifulSoup(user_r)

    # Get the number of pages the Creations are spread out on
    num_of_pages = pageme(user_soup)

    # Add the creations from page 1 to the list
    for user_link in user_soup.find_all('a'):
        if user_link.get('href')[0:49] == "/en-us/Community/CreationLab/DisplayCreation.aspx":
            creations.append('http://universe.lego.com{0}'.format(
                user_link.get('href')))

    # If there is more than one page of Creations,
    # add the creations from the other pages to the list
    if num_of_pages > 1:

        # Multiple page URL skeleton
        page_url = "{0}{1}".format(user_url[:-1], num_of_pages)

        # Update the page number (in reverse)
        while num_of_pages != 0:

            # Properly reconstruct the page number URL
            # There are more than 9 pages
            if len(str(num_of_pages)) >= 2:
                new_url = page_url[:-2]

            # There are 9 or less pages
            elif len(str(num_of_pages)) == 1:

                # Make sure we are updating the page number correctly
                if page_url[-2] != "=":
                    new_url = page_url[:-2]
                else:
                    new_url = page_url[:-1]

            # Add the Creations from each page to the list
            page_url = "{0}{1}".format(new_url, num_of_pages)
            req = requests.get(page_url).content
            soup = BeautifulSoup(req)
            for page_link in soup.find_all('a'):
                if page_link.get('href')[0:49] == "/en-us/Community/CreationLab/DisplayCreation.aspx":
                    creations.append('http://universe.lego.com{0}'.format(
                        page_link.get('href')))
            num_of_pages -= 1

    # Get the number of Creations, copy value for later usage
    num_of_creations = len(creations)
    number_of_fun = num_of_creations

    while num_of_creations > 0:
        r = requests.get(creations[num_of_creations - 1]).content
        soup = BeautifulSoup(r)

        title = soup.find_all('h1')[2]
        # Add .string to get only the text
        titleString = title.string
        titleString = titleString.replace('/', '')
        titleString = titleString.strip()
        description = soup.find(id="creationInfoText")
        tags = soup.find_all(class_='column-round-body')[3].contents[9]
        challenge = soup.find(id="CreationChallenge").contents[1].contents[1]
        date = soup.find(id="CreationUser")

        # Adapt date line for Labs from LEGO Universe competitions
        try:
            date.div.decompose()
            lucl = True
        except AttributeError:
            lucl = False
        try:
            date.img.decompose()
        except AttributeError:
            pass
        date.a.decompose()

        # Create string versions of the text
        title_str = str(title)
        description_str = str(description)
        date_str = str(date)
        tags_str = str(tags)

        # ------------ Begin Original HTML Updates ------------ #

        title_str = title_str.replace("</h1>", "")
        title_str = '{0} - Created by <a target="_blank" href="{1}{2}.aspx">{2}</a></h1>'.format(
            title_str, "http://mln.lego.com/en-us/PublicView/", localUserName)
        description_str = description_str.replace("</br></br></br></br></br></br>", "")
        description_str = description_str.replace("\t\t\t\t\t\t\t\t\t", "")
        description_str = description_str.replace('''
    \t\t\t\t\t\t\t\t''', "")
        tags_str = tags_str.lstrip('''<p>
    </p>''')
        date_str = date_str.replace("\t\t\t\t\t\t\t\t\t", "")
        date_str = date_str.replace("<br/>", "")
        date_str = date_str.replace("\t\t\t\t\t\t\t\t", "")
        date_str = date_str.replace('''<div class="column-round-body" id="CreationUser">
    <p>''', "")
        date_str = date_str.replace('''
    ''', "")
        if lucl:
            date_str = date_str.replace('<div class="column-round-body" id="CreationUser">', "")
        tags_str = tags_str.replace(r'href="',
                                    r'target="_blank" href="http://universe.lego.com/en-us/community/creationlab/')
        # If there are tags present, fix the first URL
        if tags_str != "":
            if not tags_str.startswith("<"):
                tags_str = "<{0}".format(tags_str)
        # Remove leftover closing div tag
        date_str = date_str.replace(r"</div>", "")

        # ------------ End Original HTML Updates ------------ #

        # List of non-HTML files to download
        imgLinkList = []
        i = 1

        # Populate the list
        for imgLink in soup.find_all('a'):
            if imgLink.get('href')[0:13] == "GetMedia.aspx":
                imgLinkList.append(
                    'http://universe.lego.com/en-us/community/creationlab/{0}'
                    .format(imgLink.get('href')))

        # ------------ End Creation Gathering ------------ #

        # ------------ Begin Creation Writing ------------ #

        # The folders to which the creations will be saved
        mainfolder = os.path.join(os.getcwd(), localUserName)

        # Check for illegal characters in the creation title
        subfolder = charCheck(titleString, True)
        subfolder = os.path.join(mainfolder, subfolder)

        # If the folder for each Creation does not exist, create it
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        # List of images in Creation
        image_list = []

        for imgLink in imgLinkList:
            r = requests.get(imgLink)
            img = r.content

            # Original filename
            filename = "{0}-{1}.tmp".format(titleString, i)

            # Check for illegal characters in the filenames
            filename = charCheck(filename)

            #FIXME: Complete skipping code
            ##os.chdir(subfolder)
            ##print(os.getcwd())
            #mylist = os.listdir(subfolder)
            #len_mylist = len(mylist) - 1
            #while len_mylist != -1:
                #if mylist[len_mylist].endswith("html"):
                    #del mylist[len_mylist]
                #len_mylist -= 1

            #mylist2 = []
            #for item in mylist:
                ##if not item.endswith("html"):
                #mylist2.append(item[:-4])
            #print(mylist)
            #
            #print(image_list)
            #print("\n\n", mylist2)
            #raise SystemExit(0)

            #if filename[:-4] in mylist2:
                #for ima in mylist:
                    #if ima not in image_list:
                        #image_list.append(ima)
                        ##num_of_creation_files += 1
                        ##i += 1

                #print(mylist)
                #print(image_list)

            #elif not filename[:-4] in mylist2:
                #print("not exists")
                ##i -= 1

            # Write all non-HTML files.
            with open(os.path.join(subfolder, filename), 'wb') as newImg:
                newImg.write(img)

            # ------------ Begin File Type Detection ------------ #

            #  This is an GIF image
            if imghdr.what(os.path.join(subfolder, filename)) == "gif":
                new_filename = "{0}.gif".format(filename[:-4])
                os.replace(os.path.join(subfolder, filename),
                           os.path.join(subfolder, new_filename))

            # This is an JPG image
            elif imghdr.what(os.path.join(subfolder, filename)) == "jpeg":
                new_filename = "{0}.jpg".format(filename[:-4])
                os.replace(os.path.join(subfolder, filename),
                           os.path.join(subfolder, new_filename))

            else:
                # Read the first 5 bytes of the file
                with open(os.path.join(subfolder, filename), "rb") as f:
                    header = f.readline(5)

                # This is an LDD LXF model <http://ldd.lego.com/>
                if header == b"PK\x03\x04\x14":
                    new_filename = "{0}.lxf".format(filename[:-4])
                    os.replace(os.path.join(subfolder, filename),
                               os.path.join(subfolder, new_filename))

                # This is an WMV video
                elif header == b"0&\xb2u\x8e":
                    new_filename = "{0}.wmv".format(filename[:-4])
                    os.replace(os.path.join(subfolder, filename),
                               os.path.join(subfolder, new_filename))

                # This is an MPG video
                elif header == b"\x00\x00\x01\xba!":
                    new_filename = "{0}.mpg".format(filename[:-4])
                    os.replace(os.path.join(subfolder, filename),
                               os.path.join(subfolder, new_filename))

                # This is an AVI video
                # NOTE: This was found in an H.264 AVI file
                elif header == b"\x00\x00\x00\x1cf":
                    new_filename = "{0}.mpg".format(filename[:-4])
                    os.replace(os.path.join(subfolder, filename),
                               os.path.join(subfolder, new_filename))

                # This is MOV video
                else:
                    new_filename = "{0}.mov".format(filename[:-4])
                    os.replace(os.path.join(subfolder, filename),
                               os.path.join(subfolder, new_filename))

                """
                The AVI and MOV file type is a container, meaning
                different types of codecs (what the real format is) can vary.
                Becauase of this, AVI and MOV file detection is a bit fuzzy.
                """

                # ------------ End File Type Detection ------------ #

            # Display filename after it was installed,
            # part of LUCA's non-GUI progress bar.
            try:
                print(new_filename)
            # If the filename contains Unicode characters
            except UnicodeEncodeError:
                print("Filename display error. Creation saved!")
                pass

            # Update various values
            num_of_creation_files += 1
            i += 1
            image_list.append(new_filename)
        img_num = len(image_list)

        # Original HTML filename
        HTMLfilename = "{0}.html".format(titleString)

        # Check for illegal characters in the filenames
        HTMLfilename = charCheck(HTMLfilename)

        # HTML document structure
        page = '''<!-- Creation archive saved by LUCA v{11}{12} on {0} UTC
https://github.com/Brickever/LUCA#readme
https://github.com/le717/LUCA#readme -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{1}</title>
    <style>
    {2}
    {3}
    {4}
    {5}
    </style>
</head>

<body>
{6}
<div class="line-separator"></div>

<h2>Challenge</h2>
<p>{8}
<br>Submitted {9}
<div class="line-separator"></div>

<h2>Description</h2>
{10}

<h2>Images</h2>
<div id="pictures">'''.format(
            time.strftime("%c", time.gmtime()), titleString,
            '''body { background-color: #212121;
        color: white;
        text-align: center;
        }''',
            "h1, h2 {font-family: sans-serif; }",
            '''.line-separator {
        height:1px; background:#717171;
        border-bottom:1px solid #313030;
        }''',
            "a { color: #A9A9A9; text-decoration: none;}",
            title_str, localUserName, challenge, date_str, description_str,
            majver, minver)

        # Write initial HTML document structure
        # Write all HTML using binary mode to sooth Unicode characters
        with open(os.path.join(subfolder, HTMLfilename), "wb") as newHTML:
            newHTML.write(byteme(page))

        im = 0
        while im < img_num:

            # Code to display every image
            img_display = '''
<a title="Click for larger image" href="{0}"><img src="{0}" width="300" /></a>'''.format(
                image_list[im])

            # Write the HTML for the images
            with open(os.path.join(
                      subfolder, HTMLfilename), "ab") as updateHTML:
                updateHTML.write(byteme("{0}".format(img_display)))
            # Display each image once
            im += 1

        # Write the final HTML code
        with open(os.path.join(subfolder, HTMLfilename), "ab") as finishHTML:
            finishHTML.write(byteme('''
</div>
<br>
<div class="line-separator"></div>
<br>
Original Creation Link
<br>
<a href="{0}" target="_blank">{0}</a>
<br>
<br>
Tags
<br>
{1}
</body>
</html>
    '''.format(creations[num_of_creations - 1], tags_str)))

        # Display filename after it was installed,
        # part of LUCA's non-GUI progress bar.
        try:
            print(HTMLfilename)
        # If the filename contains Unicode characters
        except UnicodeEncodeError:
            print("Filename display error. Creation saved!")
            pass
        # Update various values
        num_of_creation_files += 1
        num_of_creations -= 1

    # ------------ End Creation Writing ------------ #

    # Display success message containing number
    # of files downloaded from number of Creations, and where they were saved.
    print('''
{0} files from {1} Creations successfully downloaded and saved to
"{2}"'''.format(num_of_creation_files, number_of_fun, mainfolder))
    input("\nPress Enter to close LUCA.")

    # Delete unneeded lists to free up system resources
    del creations[:]
    del imgLinkList[:]
    del image_list[:]
    raise SystemExit(0)

    # ------------ End Final Actions ------------ #

if __name__ == "__main__":
    # Write window title
    os.system("title {0} v{1}{2}".format(app, majver, minver))
    main()
