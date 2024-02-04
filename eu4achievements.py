from urllib.request import urlopen
from urllib.parse import quote 
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import random
import logging

logger = logging.getLogger(__name__)

def privateCollectAchievements(page):
    achievements = []

    soup = BeautifulSoup(page, features='lxml')
    achievementContainer = soup.body.find_all('div', class_='achieveRow')

    for i, r in enumerate(achievementContainer):
        textContainer = r.find('div', class_='achieveTxt')

        title = textContainer.find('h3').text
        description = textContainer.find('h5').text

        unlocked = False
        if r.find('div', class_='achieveUnlockTime'):
            unlocked = True
            
        achievements.append({'title': title, 'description': description, 'unlocked': unlocked})

    return achievements


def collectAchievements(user):
    logger.info(f'Collecting achievements for user: {user}')

    linkCustom = f'https://steamcommunity.com/id/{user}/stats/236850/achievements/'
    linkDefault = f'https://steamcommunity.com/profiles/{user}/stats/236850/achievements/'

    logger.info(f'Trying link: {linkDefault}')
    pageDefault = urlopen(linkDefault)
    achievements = privateCollectAchievements(pageDefault)
    logger.info(f'Found {len(achievements)} achievements')
    if achievements != []:
        return achievements

    logger.info(f'Trying link: {linkCustom}')
    pageCustom = urlopen(linkCustom)
    achievements = privateCollectAchievements(pageCustom)    
    logger.info(f'Found {len(achievements)} achievements')
    if achievements != []:
        return achievements


def collectAchievementsDifficulty():
    logger.info('Collecting achievements difficulty')

    link = 'https://eu4.paradoxwikis.com/Achievements'

    page = urlopen(link)
    soup = BeautifulSoup(page, features='lxml')

    achievements = []

    for i, r in enumerate(soup.body.find_all('tr')):
        if i == 0:
            continue

        # title = r.find('td').text
        # difficulty = r.find_all('td')[1].text

        # achievements.append({'title': title, 'difficulty': difficulty})

    return achievements


def parseArgs():
    parser = ArgumentParser()

    parser.add_argument('-u', '--user', 
                        required=True, 
                        help='specify user to list achievements for (the id from the steamcommunity.com profile url)')
    parser.add_argument('-f', '--filter',
                        choices=['completed', 'not-completed', 'very-easy', 'easy', 'medium', 'hard', 'very-hard', 'insane', 'uncategorized'
                                 'c', 'nc', 've', 'e', 'm', 'h', 'vh', 'i', 'uc'],
                        nargs='+',
                        help='filter achievements by specified criteria')
    parser.add_argument('-r', '--random', 
                        action='store_true',
                        default=False, 
                        help='list random achievement')
    parser.add_argument('-l', '--link',
                        action='store_true',
                        default=False,
                        help='print link to eu4.paradoxwikis.com for each achievement')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='enable verbose logging')

    return parser.parse_args()

def formattedLink(title):
    return f'https://eu4.paradoxwikis.com/Achievements#List_of_achievements#:~:text={quote(title)}'

def formattedResult(achievement, link=None):
    if link:
        return f'{achievement["title"]}: {achievement["description"]}\n|> {formattedLink(achievement["title"])}'

    return f'{achievement["title"]}: {achievement["description"]}'
    

def main():
    args = parseArgs()

    user = args.user
    filter = args.filter
    pickRandom = args.random
    link = args.link
    verbose = args.verbose

    if verbose:
        logging.basicConfig(level=logging.INFO)

    logger.info(f'filter: {filter}')

    achievements = collectAchievements(user)

    if achievements == []:
        print(f'No achievements found for the user: {user}...')
        return

    if filter:
        if 'completed' in filter or 'c' in filter:
            achievements = [a for a in achievements if a['unlocked']]
            logger.info(f'Filtered for completed achievements, found: {len(achievements)}')
        if 'not-completed' in filter or 'nc' in filter:
            achievements = [a for a in achievements if not a['unlocked']]
            logger.info(f'Filtered for not completed achievements, found: {len(achievements)}')
        if 'very-easy' in filter or 've' in filter:
            pass
        if 'easy' in filter or 'e' in filter:
            pass
        if 'medium' in filter or 'm' in filter:
            pass
        if 'hard' in filter or 'h' in filter:
            pass
        if 'very-hard' in filter or 'vh' in filter:
            pass    
        if 'insane' in filter or 'i' in filter:
            pass
        if 'uncategorized' in filter or 'uc' in filter:
            pass

    if pickRandom:
        achievement = random.choice(achievements)
        print(formattedResult(achievement, link))
    else:
        print(f'Total: {len(achievements)}')
        for achievement in achievements:
            print(formattedResult(achievement, link))


if __name__ == '__main__':
    main()
