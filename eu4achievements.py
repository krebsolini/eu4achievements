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

        title = textContainer.find('h3').text.strip().replace('…', '...').replace('’', "'")

        if (title == 'Brentry'):
            title = 'Brentry!'

        description = textContainer.find('h5').text.strip()

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

    table = soup.body.find('table')

    for i, e in enumerate(table.find_all('tr')):
        if i == 0:
            continue

        title = e.find('span').get('id').replace('_', ' ').strip().replace('…', '...').replace('’', "'")
        difficulty = e.text.strip().split('\n')[-1].strip()
        
        achievements.append({'title': title, 'difficulty': difficulty})

    return achievements


def parseArgs():
    parser = ArgumentParser()

    parser.add_argument('-u', '--user', 
                        required=True, 
                        help='specify user to list achievements for (the id from the steamcommunity.com profile url)')
    parser.add_argument('-f', '--filter',
                        choices=['completed', 'not-completed', 'very-easy', 'easy', 'medium', 'hard', 'very-hard', 'insane', 'uncategorized',
                                 'c', 'nc', 've', 'e', 'm', 'h', 'vh', 'i', 'uc'],
                        nargs='+',
                        help='filter achievements by specified criteria')
    parser.add_argument('-r', '--random', 
                        action='store_true',
                        default=False, 
                        help='print only one random achievement')
    parser.add_argument('-l', '--link',
                        action='store_true',
                        default=False,
                        help='print link to eu4.paradoxwikis.com for each achievement')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='enable verbose logging')
    parser.add_argument('--no-output',
                        action='store_true',
                        default=False,
                        help='disable output')

    return parser.parse_args()

def formattedLink(title):
    return f'https://eu4.paradoxwikis.com/Achievements#{title.replace(" ", "_")}'

def formattedResult(achievement, link=None):
    try:
        if link:
            return f'[{achievement["difficulty"]}] {achievement["title"]}:\n|> {achievement["description"]}\n|> {formattedLink(achievement["title"])}'

        return f'[{achievement["difficulty"]}] {achievement["title"]}:\n|> {achievement["description"]}'
    
    except KeyError:
        logger.error(f'KeyError: {achievement}')

def main():
    args = parseArgs()

    user = args.user
    filter = args.filter
    pickRandom = args.random
    link = args.link
    verbose = args.verbose
    noOutput = args.no_output

    if verbose:
        logging.basicConfig(level=logging.INFO)

    logger.info(f'filter: {filter}')

    achievements = collectAchievements(user)
    difficulties = collectAchievementsDifficulty()

    logger.info(f'Merging achievements with difficulties')
    lookup = {item['title']: item for item in difficulties}
    achievements = [{**item, **lookup.get(item['title'], {})} for item in achievements]

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

        allowedDifficulties = []
        if 'very-easy' in filter or 've' in filter:
            allowedDifficulties.append('VE')
        if 'easy' in filter or 'e' in filter:
            allowedDifficulties.append('E')
        if 'medium' in filter or 'm' in filter:
            allowedDifficulties.append('M')
        if 'hard' in filter or 'h' in filter:
            allowedDifficulties.append('H')
        if 'very-hard' in filter or 'vh' in filter:
            allowedDifficulties.append('VH')
        if 'insane' in filter or 'i' in filter:
            allowedDifficulties.append('I')
        if 'uncategorized' in filter or 'uc' in filter:
            allowedDifficulties.append('UC')

        if allowedDifficulties:
            achievements = [a for a in achievements if a['difficulty'] in allowedDifficulties]
            logger.info(f'Filtered for difficulties: {allowedDifficulties}, found: {len(achievements)}')

    if pickRandom:
        achievement = random.choice(achievements)
        text = formattedResult(achievement, link)
        if not noOutput:
            print(text)
    else:
        print(f'Total: {len(achievements)}')
        for achievement in achievements:
            text = formattedResult(achievement, link)
            if not noOutput:
                print(text)

if __name__ == '__main__':
    main()
