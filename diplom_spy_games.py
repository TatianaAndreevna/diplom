import requests
import json
import time


access_token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
version = '5.92'


class Victim:

    def __init__(self, victim_id):
        if str(victim_id).isdigit():
            self.victim_id = victim_id
        else:
            params = {
                'user_ids': victim_id,
                'access_token': access_token,
                'v': version,
            }
            response = requests.get('https://api.vk.com/method/victims.get', params)
            victim_information = response.json()
            self.victim_id = victim_information['response'][0]['id']

    def friends(self):
        params = {
            'user_id': self.victim_id,
            'access_token': access_token,
            'v': version,
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
            'user_id': self.victim_id,
            'extended': '1',
            'access_token': access_token,
            'v': version,
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
            'access_token': access_token,
            'v': version,
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        group_info = response.json()
        return group_info


def suitable_groups():
    victim = Victim(171691064)
    victim_friends = victim.friends()
    victim_groups = victim.groups()
    total_set = set()
    for friend in victim_friends:
        time.sleep(0.3)
        flag = True
        while flag:
            try:
                i_victim = Victim(str(friend))
                total_set = total_set.union(i_victim.groups())
                print('-')
                flag = False
            except KeyError:
                print('-')

    suitable = victim_groups.difference(total_set)
    return suitable


def search_results(group_id_, file):
    group_list = []
    for group in group_id_:
        this_group = Group(str(group))
        group_info = this_group.group_information()
        iter_dict = dict()

        try:
            for item in group_info['response']:
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
