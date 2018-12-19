import requests
import json
import time


class Victim:

    def __init__(self, victim_id):
        if str(victim_id).isdigit():
            self.victim_id = victim_id
        else:
            params = {
                'victim_id': victim_id,
                'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
                'v': '5.92',
            }
            response = requests.get('https://api.vk.com/method/victims.get', params)
            victim_information = response.json()
            self.victim_id = victim_information['response'][0]['id']

    def friends(self):
        params = {
            'victim_id': self.victim_id,
            'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
            'v': '5.92',
            'fields': 'domain'
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_information = response.json()
        friends_set = set()
        for friend in friend_information['response']['items']:
            friends_set.add(friend['id'])
        return friends_set

    def groups(self):
        params = {
            'victim_id': self.victim_id,
            'extended': '1',
            'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
            'v': '5.92',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        group_information = response.json()
        group_set = set()
        for group in group_information['response']['items']:
            group_set.add(group['id'])
        return group_set


class Group:

    def __init__(self, group_id):
        self.group_id = group_id

    def group_information(self):
        params = {
            'group_id': self.group_id,
            'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
            'v': '5.92',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        group_information = response.json()
        return group_information


def suitable_groups():
    victim = Victim('171691064')
    victim_friends = victim.friends()
    victim_groups = victim.groups()

    total_set = set()
    for friend in victim_friends:
        try:
            i_victim = Victim(str(friend))
            total_set = total_set.union(i_victim.groups())
            print('-')
            time.sleep(0.1)
        except KeyError:
            print('-')
            time.sleep(0.1)

    suitable_groups = victim_groups.difference(total_set)
    return suitable_groups


def search_results(group_id_, file):
    group_list = []
    for group in group_id_:
        this_group = Group(str(group))
        group_information = this_group.group_information()
        iter_dict = dict()

        try:
            for item in group_information['response']:
                iter_dict['name'] = item['name']
                iter_dict['gid'] = item['id']
                iter_dict['members_count'] = item['members_count']
        except KeyError:
            print('-')

        group_list.append(iter_dict)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    search_results(suitable_groups(), 'groups.json')