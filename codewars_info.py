import requests
# import json
from bs4 import BeautifulSoup
from datetime import datetime as dt


def get_total(usr):
    res = requests.get(
        'https://www.codewars.com/api/v1/users/{}'.format(usr)).json()
    return [f'{res.get("username")} ({res.get("name")})',
            res.get('codeChallenges').get('totalCompleted'), res.get("honor")]


def get_task_list(usr, total):
    tasks = []
    str_url = 'https://www.codewars.com/api/v1/users/{}/code-challenges/completed?page={}'  # noqa: E501
    for page in range(total // 200 + 1):
        res = requests.get(str_url.format(usr, page))
        tasks += res.json().get('data')
    return tasks


def get_task_rank(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return soup.find('div', class_='flex items-center').find('span').get_text()


def user_codewars_tasks(compare_user):
    user = 'Gh0stik'
    usrname, totalComplite, honor = get_total(user)

    main_tasks = get_task_list(user, totalComplite)
    id_list = []
    for x in main_tasks:
        id_list.append(x.get('id'))

    jsn = []
    jsn.append({'user': user, 'honor': honor, 'total': totalComplite})

    usrname, totalComplite, honor = get_total(compare_user)
    tasks = get_task_list(compare_user, totalComplite)

    task_dict = {}
    for t in tasks:
        if t.get('id') not in id_list:
            task_url = f'https://www.codewars.com/kata/{t.get("id")}'
            task_time = t.get("completedAt")
            task_time = task_time[:task_time.find('T')]
            task_time = dt.strptime(task_time, '%Y-%m-%d').date().strftime('%d/%m/%Y')  # noqa: E501
            task_lang = ','.join(t.get("completedLanguages"))
            kyu = get_task_rank(task_url)
            if kyu != 'Retired':
                if kyu in task_dict.keys():
                    # task_dict.get(kyu).append(task_url)
                    task_dict[kyu][task_url] = f'{task_time} => {task_lang}'
                else:
                    task_dict[kyu] = {task_url: f'{task_time} => {task_lang}'}

    all = {'all': sum(len(task_dict.get(key)) for key in task_dict.keys())}
    bykyu = {f'{key}': len(task_dict.get(key)) for key in sorted(task_dict.keys())}
    jsn_item = {
        'user': usrname,
        'honor': honor,
        'total': totalComplite,
        'differences': {**all, **bykyu},
        'tasks': sorted(task_dict.items())
    }
    if (jsn_item.get('differences').get('all') == 0):
        jsn_item.pop('differences')
        jsn_item.pop('tasks')

    res = f'*{jsn_item.get("user")}*\n\nhonor: {jsn_item.get("honor")}\ntotal: {jsn_item.get("total")}'
    if not jsn_item.get("differences", None) is None:
        res += '\n\n===============  differences  ==============='
        for item in jsn_item.get("tasks"):
            res += f'\n===  {item[0]}  ===\n'
            res += '\n'.join(f'{i:02d}. {link}' for i, link in enumerate(item[1], 1))
        res += '\n===============  differences  ==============='
    return res
