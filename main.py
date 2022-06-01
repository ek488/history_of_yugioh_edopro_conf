import datetime
import json

class Expansion:
    def __init__(self, set_code, na_release_date):
        self.set_code = set_code
        self.na_release_date = na_release_date

def main(date, episode_number, episode_title):
    EDOProConfig = []

    # prepend '0' to months and days 0..9, inclusive
    if date.month < 10:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = '0' + str(date.day)
    else:
        day = str(date.day)

    EDOProConfig.append("#[" + str(date.year) + '.' + month + '.' + day + " History #" + str(episode_number) + " | " + episode_title + "]\n")
    EDOProConfig.append("!" + str(date.year) + '.' + month + '.' + day + " History #" + str(episode_number) + " | " + episode_title + "\n")
    EDOProConfig.append("$whitelist\n")

    # sets the banlist to the latest one on or before the episode date
    banlist = forbidden_and_limited_lists[0]
    for f in forbidden_and_limited_lists:
        if f <= date and f >= banlist:
            banlist = f

    for expansion in expansions:
        # checks if the expansion was released on or before the episode date
        # TODO: refactor
        if expansion.na_release_date <= date:
            exp = open("json/set_json/" + expansion.set_code + ".json")
            fal = open("json/banlist_json/" + str(banlist.year) + '_' + str(banlist.month) + ".json")
            # returns JSON object as a dictionary
            e_data = json.load(exp)
            f_data = json.load(fal)['status'][0]
            #print(f_data)

            for card in e_data['data']:
                EDOProConfig.append(str(card['id']))
                num_copies = 3
                for focard in f_data['forbidden']:
                    if focard['id'] == card['id']:
                        num_copies = 0
                for licard in f_data['limited']:
                    if licard['id'] == card['id']:
                        num_copies = 1
                for slcard in f_data['semi-limited']:
                    if slcard['id'] == card['id']:
                        num_copies = 2
                EDOProConfig.append(" " + str(num_copies) + "\n")

            with open("EDOPro_conf/History_" + str(episode_number) + ".conf", 'w') as f:
                f.writelines(EDOProConfig)

            exp.close()

# TODO: change to array
expansions = {
    Expansion("LOB", datetime.datetime(2002, 3, 8)),
    Expansion("DDS", datetime.datetime(2002, 3, 19)),
    Expansion("SDK", datetime.datetime(2002, 3, 29)),
    Expansion("SDY", datetime.datetime(2002, 3, 29)),
    Expansion("MRD", datetime.datetime(2002, 6, 26)),
    Expansion("TP1", datetime.datetime(2002, 9, 1)),
    Expansion("MRL", datetime.datetime(2002, 9, 16)),
    Expansion("TP2", datetime.datetime(2002, 10, 1)),
    Expansion("EDS", datetime.datetime(2002, 10, 15)),
    Expansion("PSV", datetime.datetime(2002, 10, 20)),
    Expansion("FMR", datetime.datetime(2002, 11, 26)),
    Expansion("MP1", datetime.datetime(2002, 12, 20))
}

forbidden_and_limited_lists = [
    datetime.datetime(2002, 3, 8), # No banlist
    datetime.datetime(2002, 5, 7), # May 7, 2002
    datetime.datetime(2002, 7, 1), # July 1, 2002
    datetime.datetime(2002, 10, 1), # October 1, 2002
    datetime.datetime(2002, 12, 1) # October 1, 2002
]

main(datetime.datetime(2002, 3, 8), 1, "The Legend of Blue-Eyes White Dragon")
main(datetime.datetime(2002, 3, 29), 2, "Starter Deck Yugi & Starter Deck Kaiba")
main(datetime.datetime(2002, 5, 7), 3, "The First Limited List")
main(datetime.datetime(2002, 6, 26), 4, "Metal Raiders")
main(datetime.datetime(2002, 9, 1), 5, "Mechanicalchaser & Tournament Pack 1")
main(datetime.datetime(2002, 9, 16), 6, "Magic Ruler / Spell Ruler")
main(datetime.datetime(2002, 10, 1), 7, "Morphing Jar & Tournament Pack 2")
main(datetime.datetime(2002, 10, 20), 8, "Pharaoh's Servant")
main(datetime.datetime(2002, 12, 1), 9, "The End of 2002")
