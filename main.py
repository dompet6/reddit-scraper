import bs4 as bs
import urllib.request
import requests
import praw
import os, datetime, sys


def downloadIMG(url, name):
    urllib.request.urlretrieve(url, name)

def initConfig():
    global sub, maxPosts, savePath, password, username, sortby, secretID, publicID, imgCounter
    imgCounter = 0

    # get config ini, to specify subreddit, maximum number of posts and where to save the images
    configINI = open('config.ini', 'r')
    configArgs = configINI.read().split('\n')

    if '-manual' in sys.argv:
        sub = input('Enter subreddit: ')
        maxPosts = input('\nEnter maximum number of downloads: ')
        sortby = input('\nEnter sorting method: ')
        username = input('\nEnter reddit username: ')
        password = input('\nEnter reddit password: ')

    # check through the config.ini arguments and assign them to the correct variables
    for configArg in configArgs:
        if '-manual' not in sys.argv:
            if 'subreddit' in configArg:
                sub = configArg[configArg.index('=') + 1:]

            elif 'maxPosts' in configArg:
                maxPosts = int(configArg[configArg.index('=') + 1:])

            elif 'savePath' in configArg:
                savePath = configArg[configArg.index('=') + 1:]

            elif 'password' in configArg:
                password = configArg[configArg.index('=') + 1:]

            elif 'username' in configArg:
                username = configArg[configArg.index('=') + 1:]

            elif 'sortby' in configArg:
                sortby = configArg[configArg.index('=') + 1:]

            elif 'secretID' in configArg:
                secretID = configArg[configArg.index('=') + 1:]

            elif 'publicID' in configArg:
                publicID = configArg[configArg.index('=') + 1:]

        if 'secretID' in configArg:
            secretID = configArg[configArg.index('=') + 1:]

        elif 'publicID' in configArg:
            publicID = configArg[configArg.index('=') + 1:]

        elif ('savePath') in configArg:
            savePath = configArg[configArg.index('=') + 1:]


def getSubmissions(sub, sorting):
    if 'top_' in sortby:
        if 'day' in sortby or 'week' in sortby or 'month' in sortby or 'year' in sortby or 'all' in sortby:
            return subreddit.top(sortby[sortby.index('_') + 1:], limit=maxPosts)
        else:
            print('INCORRECT SORTING DEFINED')
            input('Press Enter to exit...')
            exit(1)


    elif 'hot' in sortby:
        return subreddit.hot(limit=maxPosts)

    elif 'new' in sortby:
        return subreddit.new(limit=maxPosts)

    elif 'controversial' in sortby:
        return subreddit.controversial(limit=maxPosts)

    else:
        print('INCORRECT SORTING DEFINED')
        input('Press Enter to exit...')
        exit(1)


def checkSubmissions(submissions, filepath):
    global imgCounter
    for submission in submissions:
        if 'imgur.com/' not in submission.url:
            # the link is not an imgur link
            if 'i.redd.it' in submission.url:
                downloadIMG(submission.url, filepath + '_' + str(imgCounter) + '.png')
                imgCounter += 1


            else:
                print("Not Imgur/redd.it")


        elif 'i.imgur.com/' in submission.url:
            # the link is a direct link to an image
            downloadIMG(submission.url, filepath + '_' + str(imgCounter) + '.png')
            imgCounter += 1


        elif 'http://imgur.com/' in submission.url:
            # The link ist to an imgur page with 1 image
            source = requests.get(submission.url).text  # get imgur source
            bsSource = bs.BeautifulSoup(source, 'html.parser')
            imageURL = 'https:' + bsSource.select('img')[0]['src']
            downloadIMG(imageURL, filepath + '_' + str(imgCounter) + '.png')
            imgCounter += 1

        elif 'imgur.com/a/' in submission.url or 'imgur.com/gallery/' in submission.url:
            # The link is an album with multiple images
            source = requests.get(submission.url).text
            soup = bs.BeautifulSoup(source, 'html.parser')
            for tag in soup.select('img'):
                if 'i.imgur.com' in tag['src']:
                    imageURL = tag['src']
                    downloadIMG('https:' + imageURL, filepath + '_' + str(imgCounter) + '.png')
                    imgCounter += 1


initConfig()


# while os.path.exists(savePath + '/' + filename + '-' + str(imgCounter) + '.png'):
#     imgCounter += 1

#create a reddit instance, so we can connect to reddit
reddit = praw.Reddit(client_id=publicID,
                     client_secret = secretID,
                     user_agent = 'Wallpaper bot by u/YeeIsLoveYeeIsLife',
                     username = username,
                     password = password)

subreddit = reddit.subreddit(sub)


submissions1 = getSubmissions(subreddit, sortby)


#Add a folder with the current date to the path
filename = str(datetime.datetime.now().day) + '.' + str(datetime.datetime.now().month) + '_' + sortby
savePath += '/' + sub + '/' + filename
print(savePath)

#Create a new directory in the save path according to the subreddit and the date if it doesnt exist yet
if not os.path.exists(savePath):
    print('CREATED DIRECTORY')
    os.makedirs(savePath)

savePath += '/' + filename

checkSubmissions(submissions1, savePath)

#go through each submission and download the image if possible

print('%d Images downloaded !' %(imgCounter))
input('Press Enter to exit...')






