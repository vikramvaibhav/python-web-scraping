# -*- coding: utf-8 -*-
import requests as req
from bs4 import BeautifulSoup as bs
import lxml
from pathlib import Path
# csv writer
import pandas as pd
import time

from .config import BASE_DIR, BASE_URL

# import functions from common.py
from .common import (initialize, get_chrome_driver, makedirs,
                     get_logger, csv2xl, get_session, write_json)
# function for getting product_rating & reviews


def product_rating(url):
    base_url = 'https://widget.trustpilot.com/trustboxes/5763bccae0a06d08e809ecbb/index.html'
    driver = get_chrome_driver()
    driver.get(base_url+url)
    time.sleep(3)
    soup = bs(driver.page_source.encode('utf-8'), 'lxml')
    time.sleep(3)
    star_rating = soup.find(
        'div', {'class': 'tp-widget-summary__rating'}).find('span', {'class': 'rating'}).text
    reviews = soup.find('div', {'class': 'tp-widget-reviews'}
                        ).find_all('div', {'class': 'tp-widget-review'})
    final_review_text = ''
    for review in reviews:
        name = review.find('div', {'class': 'tp-widget-review__heading'}).find(
            'span', {'class': 'tp-widget-review__display-name'}).text+'\n'
        date = review.find(
            'div', {'class': 'tp-widget-review__date'}).text+'\n'
        review_text = review.find(
            'div', {'class': 'tp-widget-review__text'}).text+'\n\n'
        final_review_text += name+date+review_text
    return star_rating, final_review_text
# def_end


# function for getting itinerary_details
def get_itinerary(url):
    se = get_session()
    r = se.get(BASE_URL+url)
    soup = bs(r.content, 'lxml')

    itinerary = soup.find('div', {'class': 'itinerary'}).find_all(
        'div', {'class': 'day detailed'})
    detailed_itinerary = ''
    counter = 1
    for data in itinerary:
        try:
            day_number = str(counter)+'. '+data.find('span',
                                                     {'class': 'day-number'}).text+' '
            # print(day_number)
        except:
            day_number = ''
        try:
            location = data.find('span', {'class': 'location'}).text+'\n\n'
        except:
            location = ''
        try:
            summary = data.find('div', {'class': 'summary'}).text.replace(
                '  ', '').replace('\n', '')+'\n\n'
        except:
            summary = ''

        try:
            instructions = data.find('div', {'class': 'instructions'}).text.replace(
                '  ', '').replace('\n', '')+'\n\n'
        except:
            instructions = ''

        try:
            day_inclusions = data.find('div', {'class': [
                                       'day-inclusions', 'meals']}).text.replace('  ', '').replace('\n', '')+'\n\n'
        except:
            day_inclusions = ''
        try:
            details = data.find('div', {'class': 'details'}).text
            components = data.find_all('div', {'class': 'components'})
            optional_activity_data = ''
            transport_final = ''
            land_tour_final = ''
            landsport_final = ''
            animal_final = ''
            watersport_final = ''
            nature_final = ''
            accommodation_final = ''
            exhibit_final = ''
            landmark_final = ''
            health_and_wellness_final = ''
            for component_data in components:

                # health_and_wellness
                try:
                    health_and_wellness_final += 'Health And Wellness: '+component_data.find('div', {'class': 'health-and-wellness'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'health-and-wellness'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # transport
                try:
                    transport_final += 'Transport: '+component_data.find('div', {'class': 'transport'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'transport'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # exhibit
                try:
                    exhibit_final += 'Exhibit: '+component_data.find('div', {'class': 'exhibit'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'exhibit'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # landmark
                try:
                    landmark_final += 'Landmark: '+component_data.find('div', {'class': 'landmark'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'landmark'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # land-tour
                try:
                    land_tour_final += 'Landtour: '+component_data.find('div', {'class': 'land-tour'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'land-tour'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # landsport
                try:
                    landsport_final += 'Landsport: '+component_data.find('div', {'class': 'landsport'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace('\n', '')+'\n'+component_data.find('div', {'class': 'landsport'}).find(
                        'div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n Price per person : '+component_data.find('div', {'class': 'landsport'}).find('div', {'class': 'c-title'}).find('span', {'class': 'budget'}).text.replace('\n', '').replace('  ', '')+'\n'
                except:
                    pass

                # animal
                try:
                    animal_final += 'Animal: '+component_data.find('div', {'class': 'animal'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'animal'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # watersport
                try:
                    watersport_final += 'Watersport: '+component_data.find('div', {'class': 'watersport'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'watersport'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n'
                except:
                    pass

                # nature
                try:
                    nature_final += 'Nature: '+component_data.find('div', {'class': 'nature'}).find('div', {'class': 'c-title'}).find('h5').text.replace('  ', '').replace(
                        '\n', '')+'\n'+component_data.find('div', {'class': 'nature'}).find('div', {'class': 'c-title'}).find('div', {'class': 'summary'}).text+'\n\n'
                except:
                    pass

                # Accommodation
                try:
                    accommodation_final += 'Accommodation: '+component_data.find(
                        'div', {'class': 'accommodation'}).find('div', {'class': 'c-title'}).find('h5').text+'\n\n'
                except:
                    pass
                optional_activity_data = transport_final + land_tour_final + landsport_final + \
                    animal_final + watersport_final + nature_final + accommodation_final + \
                    exhibit_final+landmark_final+health_and_wellness_final
            detailed_itinerary += day_number+location + \
                summary+instructions+day_inclusions+optional_activity_data
        except:
            continue
        counter += 1
    return detailed_itinerary


# def_end


# function for getting tour_details


def get_tour_details(url):
    se = get_session()
    r = se.get(BASE_URL+url)
    soup = bs(r.content, 'lxml')

    try:
        highlights = soup.find('div', {'id': 'highlights'}).find('p').text
        # print(highlights)
    except:
        highlights = ''

    try:
        dossier_disclaimer = soup.find(
            'div', {'id': 'dossier-disclaimer'}).find('p').text
        # print(dossier_disclaimer)
    except:
        dossier_disclaimer = ''

    try:
        itinerary_disclaimer = soup.find(
            'div', {'id': 'itinerary-disclaimer'}).find_all('p')
        # print(itinerary_disclaimer)
    except:
        itinerary_disclaimer = ''

    try:
        important_notes = soup.find(
            'div', {'id': 'important-notes'}).find_all('p')
        # print(important_notes)
    except:
        important_notes = ''

    try:
        group_leader_description = soup.find(
            'div', {'id': 'group-leader-description'}).find_all('p')
    except:
        group_leader_description = ''

    try:
        group_size_notes = soup.find(
            'div', {'id': 'group-size-notes'}).find_all('p')
    except:
        group_size_notes = ''

    try:
        local_flights = soup.find('div', {'id': 'local-flights'}).find_all('p')
    except:
        local_flights = ''

    try:
        what_to_take = soup.find('div', {'id': 'what-to-take'}).find_all('p')
    except:
        what_to_take = ''

    try:
        packing_list = soup.find('div', {'id': 'packing-list'}).find_all('p')
        # print(packing_list)
    except:
        packing_list = ''

    try:
        visas_requirements = soup.find(
            'div', {'id': 'visas-and-entry-requirements'}).find_all('p')
    except:
        visas_requirements = ''

    try:
        weather = soup.find('div', {'id': 'detailed-trip-notes'}).find_all('p')
    except:
        weather = ''

    try:
        optional_activities = soup.find(
            'div', {'id': 'optional-activities'}).find_all('p')
    except:
        optional_activities = ''

    try:
        travel_insurance = soup.find(
            'div', {'id': 'travel-insurance'}).find_all('p')
    except:
        travel_insurance = ''

    try:
        emergency_contact = soup.find(
            'div', {'id': 'emergency-contact'}).find_all('p')
    except:
        emergency_contact = ''

    try:
        local_dress = soup.find('div', {'id': 'local-dress'}).find_all('p')
    except:
        local_dress = ''

    try:
        physical_grading = soup.find('div', {'id': 'introduction'}).find('span', {
            'class': 'muted'}, text='Physical Grading:').parent.text.replace('Physical Grading: ', '')
    except:
        physical_grading = ''

    try:
        whats_included = soup.find(
            'div', {'id': 'whats-included'}).find_all('p')
    except:
        whats_included = ''

    return highlights, dossier_disclaimer, itinerary_disclaimer, important_notes, group_leader_description, group_size_notes, local_flights, what_to_take, packing_list, visas_requirements, weather, optional_activities, travel_insurance, emergency_contact, local_dress, physical_grading, whats_included


# Run is a driver Function.

def run(url, infod, sitename, logger):
    print(url)
    driver = get_chrome_driver()
    driver.get(url)

    soup = bs(driver.page_source.encode('utf-8'), 'lxml')

    highlights, dossier_disclaimer, itinerary_disclaimer, important_notes, group_leader_description, group_size_notes, local_flights, what_to_take, packing_list, visas_requirements, weather, optional_activities, travel_insurance, emergency_contact, local_dress, physical_grading, whats_included = get_tour_details(soup.find(
        'ul', {'id': 'trip-summary-nav'}).find_all('a')[-1]['href'])

    infod['OPERATOR NAME'].append('G Adventures')
    infod['OPERATOR WEBSITE'].append(BASE_URL)

    # adventure_name

    try:
        # print(soup.find('div', {'class': 'title-block'}
        #                 ).find('h1', {'class': 'text-center'}).text)
        infod['ADVENTURE NAME'].append(soup.find('div', {'class': 'title-block'}
                                                 ).find('h1', {'class': 'text-center'}).text)
    except:
        infod['ADVENTURE NAME'].append('')

    # trip_url

    try:
        infod['TRIP URL'].append(url)
    except:
        infod['TRIP URL'].append('')

    # continent_name

    try:
        # print(soup.find('div', {'id': 'breadcrumbs'}).find_all('a')[-2])
        infod['CONTINENT'].append(soup.find(
            'div', {'id': 'breadcrumbs'}).find_all('a')[-2].text)
    except:
        infod['CONTINENT'].append('')

    # country_name

    try:
        # print(soup.find('div', {'id': 'breadcrumbs'}).find_all('a')[-1].text)
        infod['COUNTRY'].append(soup.find(
            'div', {'id': 'breadcrumbs'}).find_all('a')[-1].text)
    except:
        infod['COUNTRY'].append('')

    # start_point and end_point

    try:
        start_finish = soup.find('div', {'class': 'duration-container'}
                                 ).find('span', {'class': 'start_finish'}).text.split(' to ')
        # print(start_finish[0])
        infod['START POINT'].append(start_finish[0])
        infod['END POINT'].append(start_finish[1])
    except:
        infod['START POINT'].append('')
        infod['END POINT'].append('')

    # trip_duration
    try:
        # print(soup.find('div', {'class': 'duration-container'}).find('span', {'class': 'duration'}).text.replace(' days', ''))
        infod['TRIP DURATION (Days)'].append(soup.find('div', {
            'class': 'duration-container'}).find('span', {'class': 'duration'}).text.replace(' days', ''))
    except:
        infod['TRIP DURATION (Days)'].append('')

    # minimum_age
    try:
        # print(soup.find('div', {'id': 'age-requirement'}).find('h3').text.replace('Age requirement: ','').replace(' ','').replace('+',''))
        infod['AGE (MIN)'].append(soup.find('div', {'id': 'age-requirement'}).find(
            'h3').text.replace('Age requirement: ', '').replace(' ', '').replace('+', ''))
    except:
        infod['AGE (MIN)'].append('')

    # adventure_overview
    try:
        # print(soup.find('div', {'id': 'trip-description'}
        #                 ).find('p', {'class': 'visible-desktop'}).text)
        infod['ADVENTURE OVERVIEW'].append(soup.find('div', {'id': 'trip-description'}
                                                     ).find('p', {'class': 'visible-desktop'}).text.replace('  ', ''))
    except:
        infod['ADVENTURE OVERVIEW'].append('')

    # highlights
    try:
        infod['HIGHLIGHTS'].append(highlights)
    except:
        infod['HIGHLIGHTS'].append('')

    # brief_itinerary_details
    try:
        itinerary = soup.find('div', {'class': 'itineraries'}
                              ).find_all('div', {'class': 'day'})
        brief_itinerary = ''
        counter = 1
        for data in itinerary:
            brief_itinerary += str(counter)+'. '+data.find('span', {'class': 'day-number'}).text+' '+data.find(
                'span', {'class': 'location'}).text+'\n'
            counter += 1
        # print(brief_itinerary)
        infod['BRIEF ITINERARY'].append(brief_itinerary)
    except:
        infod['BRIEF ITINERARY'].append('')

    # detail_itineray_details
    try:
        # print(get_itinerary(soup.find('ul', {'id': 'trip-summary-nav'}).find_all('a')[-2]['href']))
        infod['DETAILED ITINERARY'].append(get_itinerary(
            soup.find('ul', {'id': 'trip-summary-nav'}).find_all('a')[-2]['href']))
    except:
        infod['DETAILED ITINERARY'].append('')

    # weather
    try:
        weather_final = ''
        for data in weather:
            weather_final += data.text+'\n'
        infod['WEATHER'].append(weather_final)
    except:
        infod['WEATHER'].append('')

    # availability_status & departure_dates

    try:
        departure_dates = soup.find('div', {'id': 'departures-list'}
                                    ).find_all('div', {'class': 'action'})
        available_status = soup.find('div', {'id': 'departures-list'}
                                     ).find_all('div', {'class': 'avail'})
        final_status = []

        for info in available_status:
            # print(info.text)
            stripped_info = info.text.replace(
                '\n', '').replace(' ', '').replace('+', '')
            if 'Available' in stripped_info:
                final_status.append(
                    'A '+'('+stripped_info.split('\xa0')[0]+')')
        # print(final_status)
        dates = []
        for data in departure_dates:
            try:
                dates.append(data.find('a')['href'].split('#date/')[1])
            except:
                continue
            # print(data.find('a')['href'])
        # print(dates)

        dates_status_dict = dict(zip(dates, final_status))
        departure_dates_final = ''
        for date, date_status in dates_status_dict.items():
            departure_dates_final += date+' '+date_status+'\n'
        # print(departure_dates_final)
        infod['UPCOMING DEPARTURE & AVAILABILITY'].append(
            departure_dates_final)
    except:
        infod['UPCOMING DEPARTURE & AVAILABILITY'].append('')

    infod['CURRENCY'].append('USD')

    # price_per_person

    try:
        infod['PRICE PER PERSON'].append(soup.find('div', {'class': 'price'}
                                                   ).find('span', {'class': 'price'}).text)
    except:
        infod['PRICE PER PERSON'].append('')

    # booking_url

    try:
        # print(url.split('#')[0]+'pricing/')
        infod['OPERATOR BOOKING URL'].append(url.split('#')[0]+'pricing/')
    except:
        infod['OPERATOR BOOKING URL'].append('')

    # inclusions

    try:
        whats_included_final = ''
        for data in whats_included:
            whats_included_final += str(data)
        infod['INCLUSIONS'].append(whats_included_final.replace(
            '<br/>', '\n\u2022 ').replace('<p>', '\u2022 ').replace('</p>', '')+'\n')
    except:
        infod['INCLUSIONS'].append('')

    # meals

    try:
        # print(soup.find(
        #     'div', {'id': 'meals'}).find('p').text.replace('  ', ''))
        infod['MEALS'].append(soup.find(
            'div', {'id': 'meals'}).find('p').text.replace('  ', ''))
    except:
        infod['MEALS'].append('')

    # lodging_details

    try:
        # print(soup.find('div', {'id': 'accommodations'}).find('p').text)
        infod['LODGING'].append(soup.find(
            'div', {'id': 'accommodations'}).find('p').text)
    except:
        infod['LODGING'].append('')

    # transport

    try:
        # print(soup.find(
        #     'div', {'id': 'transportation'}).find('p').text)
        infod['TRANSPORT'].append(soup.find(
            'div', {'id': 'transportation'}).find('p').text)
    except:
        infod['TRANSPORT'].append('')

    infod['OTA NAME'].append('G Adventures')
    infod['OTA WEBSITE'].append(BASE_URL)

    # adventure_type

    try:
        if 'Cycling' in url.split('#')[1]:
            # print('Biking')
            infod['ADVENTURE TYPE'].append('Biking')
        elif 'Hiking & Trekking' in url.split('#')[1]:
            # print('Hiking, Trekking and Mountaineering')
            infod['ADVENTURE TYPE'].append(
                'Hiking, Trekking and Mountaineering')
        elif 'Multisport' in url.split('#')[1]:
            # print('Multisport')
            infod['ADVENTURE TYPE'].append('Multisport')
    except:
        infod['ADVENTURE TYPE'].append('')

    # adventure_subb_type

    try:
        infod['ADVENTURE SUB-TYPE'].append(url.split('#')[1])
    except:
        infod['ADVENTURE SUB-TYPE'].append('')

    # difficulty_level and grade

    try:
        infod['DIFFICULTY LEVEL - BY OPERATOR'].append(physical_grading.split(' - ')[
            0])
        infod['GRADE - BY OPERATOR'].append(physical_grading.split(' - ')[1])
    except:
        infod['DIFFICULTY LEVEL - BY OPERATOR'].append('')
        infod['GRADE - BY OPERATOR'].append('')

    # activity_style

    try:
        # print(soup.find('div', {'id': 'trip-style'}
        #                 ).find('h3').text.replace('Travel Style: ', ''))
        infod['OPERATOR ACTIVITY STYLE'].append(soup.find(
            'div', {'id': 'trip-style'}).find('h3').text.replace('Travel Style: ', ''))
    except:
        infod['OPERATOR ACTIVITY STYLE'].append('')

    # packing_list & gears

    try:
        counter = 1
        final_packing_list = ''
        for data in packing_list:
            final_packing_list += str(counter)+'. ' + \
                data.text.replace('\u2022', '\n\u2022')+'\n\n'
            # print(str(counter)+'. '+data.text.replace('\u2022','\n\u2022')+'\n')
            counter += 1
        infod['OPERATOR PACKING LIST - GEAR & DOCUMENT'].append(
            final_packing_list)
    except:
        infod['OPERATOR PACKING LIST - GEAR & DOCUMENT'].append('')

    # user_reviews

    try:
        rating, reviews = product_rating(
            soup.find('div', {'class': 'trustpilot-widget'}).find('iframe')['src'].split('index.html')[1])
        infod['USER REVIEWS'].append(reviews)
    except:
        infod['USER REVIEWS'].append('')

    # product_code

    try:
        infod['OPERATOR PRODUCT CODE'].append(soup.find(
            'div', {'class': 'trip_code'}).text.replace('Trip Code: ', ''))
    except:
        infod['OPERATOR PRODUCT CODE'].append('')

    # discounts

    try:
        infod['DISCOUNTS'].append(soup.find('div', {'class': 'p-amount'}).find('a').text.replace(
            '  ', '').replace('\n', '')+'\n'+soup.find('div', {'class': 'p-expires'}).text)
    except:
        infod['DISCOUNTS'].append('')

    # average_product_rating

    try:
        rating, reviews = product_rating(
            soup.find('div', {'class': 'trustpilot-widget'}).find('iframe')['src'].split('index.html')[1])
        infod['AVERAGE PRODUCT RATING'].append(rating)
    except:
        infod['AVERAGE PRODUCT RATING'].append('')

    # images

    try:
        # print(soup.find('img', {'class': 'page-head'})['src'])
        infod['IMAGES'].append(soup.find('img', {'class': 'page-head'})['src'])
    except:
        infod['IMAGES'].append('')

    # extra_fields

    try:
        # print(soup.find(
        #     'div', {'id': 'staff-experts'}).find('p').text)
        infod['STAFF & EXPERTS'].append(soup.find(
            'div', {'id': 'staff-experts'}).find('p').text)
    except:
        infod['STAFF & EXPERTS'].append('')
    try:
        infod['DOSSIER DISCLAIMER'].append(dossier_disclaimer)
    except:
        infod['DOSSIER DISCLAIMER'].append('')

    try:
        itinerary_disclaimer_final = ''
        for data in itinerary_disclaimer:
            itinerary_disclaimer_final += '\u2022'+data.text+'\n\n'
        # print(itinerary_disclaimer_final)
        infod['ITINERARY DISCLAIMER'].append(itinerary_disclaimer_final)
    except:
        infod['ITINERARY DISCLAIMER'].append('')

    try:
        important_notes_final = ''
        for data in important_notes:
            important_notes_final += str(data)
        infod['IMPORTANT NOTES'].append(important_notes_final.replace(
            '<p>', '').replace('</p>', '\n\n').replace('<br/>', ''))
    except:
        infod['IMPORTANT NOTES'].append('')

    try:
        group_leader_description_final = ''
        for data in group_leader_description:
            group_leader_description_final += data.text+'\n'
        infod['GROUP LEADER DESCRIPTION'].append(
            group_leader_description_final)
    except:
        infod['GROUP LEADER DESCRIPTION'].append('')

    try:
        group_size_notes_final = ''
        for data in group_size_notes:
            group_size_notes_final += data.text+'\n'
        infod['GROUP SIZE'].append(group_size_notes_final)
    except:
        infod['GROUP SIZE'].append('')

    try:
        local_flights_final = ''
        for data in local_flights:
            local_flights_final += data.text+'\n'
        # print(local_flights_final)
        infod['LOCAL FLIGHTS'].append(local_flights_final)
    except:
        infod['LOCAL FLIGHTS'].append('')

    try:
        what_to_take_final = ''
        for data in what_to_take:
            what_to_take_final += '\u2022 '+data.text+'\n\n'
        # print(what_to_take_final)
        infod['WHAT TO TAKE'].append(what_to_take_final)
    except:
        infod['WHAT TO TAKE'].append('')

    try:
        visas_requirements_final = ''
        for data in visas_requirements:
            visas_requirements_final += '\u2022 '+data.text+'\n\n'
        # print(visas_requirements_final)
        infod['VISAS REQUIREMENTS'].append(visas_requirements_final)
    except:
        infod['VISAS REQUIREMENTS'].append('')

    try:
        optional_activities_final = ''
        counter = 1
        for data in optional_activities:
            optional_activities_final += str(counter)+'. '+str(data)
            counter += 1
        # print(optional_activities_final.replace('<br/>', '\n').replace('<p>', '').replace('</p>', '\n'))
        infod['OPTIONAL ACTIVITIES'].append(optional_activities_final.replace(
            '<br/>', '\n').replace('<p>', '').replace('</p>', '\n'))
    except:
        infod['OPTIONAL ACTIVITIES'].append('')

    try:
        travel_insurance_final = ''
        for data in travel_insurance:
            travel_insurance_final += data.text
        # print(travel_insurance_final)
        infod['TRAVEL INSURANCE'].append(travel_insurance_final)
    except:
        infod['TRAVEL INSURANCE'].append('')

    try:
        emergency_contact_final = ''
        counter = 1
        for data in emergency_contact:
            emergency_contact_final += '\n\n'+str(counter)+'. '+str(data)
            counter += 1
        # print(emergency_contact_final.replace('<br/>', '\n').replace('<p>', '').replace('</p>', ''))
        infod['EMERGENCY CONTACT'].append(emergency_contact_final.replace(
            '<br/>', '\n').replace('<p>', '').replace('</p>', ''))
    except:
        infod['EMERGENCY CONTACT'].append('')

    try:
        local_dress_final = ''
        for data in local_dress:
            local_dress_final += data.text+'\n'
        # print(local_dress_final)
        infod['LOCAL DRESS'].append(local_dress_final)
    except:
        infod['LOCAL DRESS'].append('')

    driver.quit()


# function to write links to a text file

def write_link_txt(url):
    file_path = 'links_gadventures.txt'
    with open(file_path, "a") as textfile:
        textfile.write(BASE_URL+url+'\n')

# def_end


# function to get the links

def get_links(activity, link):
    se = get_session()
    r = se.get(link.format('1'))
    soup = bs(r.content, 'lxml')
    try:
        page = int(
            soup.find('div', {'class': 'pagination'}).find_all('li')[-2].text)
    except:
        page = ''
    if page:
        for x in range(1, page+1):
            r = se.get(link.format(x))
            soup = bs(r.content, 'lxml')
            link_div = soup.find('div', {'id': 'results'}).find_all(
                'a', {'class': 'trip-tile-map'})
            for result_link in link_div:
                # print(result_link['href'])
                write_link_txt(result_link['href']+'#'+activity)
    else:
        link_div = soup.find('div', {'id': 'results'}).find_all(
            'a', {'class': 'trip-tile-map'})
        for result_link in link_div:
            write_link_txt(result_link['href']+'#'+activity)

# def_end


# Execute is a root funtion it starts the scraping process.


def execute(sitename):
    makedirs(sitename)
    logger = get_logger(sitename)
    fname, infod, column_names = initialize(sitename)

    activity_dict = {'Cycling': 'https://www.gadventures.com/search/?page={}&f=a7a3ea2baafa+612e33ca252a', 'Hiking & Trekking': 'https://www.gadventures.com/search/?page={}&f=612e33ca252a', 'Multisport': 'https://www.gadventures.com/search/?page={}&f=deae81eafd2d',
                     'Multisport': 'https://www.gadventures.com/search/?page={}&f=dossier_code=CRAC&dossier_code=CRSM&dossier_code=ONAP&dossier_code=AVHB&dossier_code=ATHB&dossier_code=SPHK&dossier_code=SEGL&dossier_code=ONSA&dossier_code=SEEM&dossier_code=DCAA&dossier_code=NUAB&dossier_code=DJJA&dossier_code=NUSA'}

    # for activity, activity_id in activity_dict.items():
    #     get_links(activity, activity_id)
    infile = BASE_DIR / 'core/links_gadventures.txt'
    num_lines = sum(1 for line in open(infile))
    with open(infile, 'r') as file:
        links = file.read().splitlines()
    for idx, link in enumerate(links):
        # print(link)
        run(link, infod, sitename, logger)
        df = pd.DataFrame(infod, columns=column_names)
        # dataframe to csv
        df.to_csv(str(BASE_DIR)+'/scraping_output/'+sitename +
                  '/'+fname+'.csv', index=False, header=True)
        print("{}/{} is complete.".format(idx+1, num_lines))
        logger.error("{}/{} is complete.".format(idx+1, num_lines))
    # print(fname)

    write_json(fname, sitename)
    csv2xl(fname + '.csv', 'gadventures')
    print('Data extracted successfully...')
# def_end
