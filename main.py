import sys
from core import gadventures

total = len(sys.argv)

if total < 2:
    print('\nrequired parameter(s) missing..\n')
    sys.exit()

if total > 2:
    print('\ntoo many parameters.. one parameter expected.\n')
    sys.exit()

sitename = sys.argv[1]
switcher = {
    'gadventures': gadventures
}
driver = switcher.get(sitename)
if sitename == 'gadventures':
    # Start scraping
    driver.execute(sitename)
else:
    print('Wrong parameter passed...')
    sys.exit()
