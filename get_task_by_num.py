def get_task_by_num(num):
    from bs4 import BeautifulSoup
    import requests
    import random
    cat_dict = {
        '1': 'cat12=on&cat13=on',
        '2': 'cat8=on',
        '3': 'cat16=on',
        '4': 'cat21=on&cat22=on&cat23=on&cat25=on',
        '5': 'cat27=on&cat28=on&cat144=on',
        '6': 'cat37=on&cat91=on',
        '7': 'cat38=on&cat39=on',
        '8': 'cat42=on&cat43=on&cat145=on',
        '9': 'cat146=on&cat147=on',
        '10': 'cat148=on',
        '11': 'cat52=on&cat53=on&cat54=on&cat149=on',
        '12': 'cat55=on&cat56=on&cat57=on&cat58=on',
        '13': 'cat59=on',
        '14': 'cat60=on&cat61=on&cat62=on',
        '15': 'cat67=on&cat68=on&cat69=on&cat70=on&cat123=on',
        '16': 'cat44=on&cat45=on&cat46=on',
        '17': 'cat150=on&cat151=on',
        '18': 'cat152=on&cat153=on&cat165=on',
        '19': 'cat154=on&cat163=on',
        '20': 'cat154=on&cat163=on',
        '21': 'cat154=on&cat163=on',
        '22': 'cat73=on&cat74=on',
        '23': 'cat78=on&cat79=on&cat80=on&cat162=on',
        '24': 'cat155=on&cat156=on&cat164=on',
        '25': 'cat157=on&cat158=on&cat159=on',
        '26': 'cat160=on',
        '27': 'cat161=on',
    }
    category = cat_dict[num]
    URL = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={num}&{category}'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    center = soup.find('div', class_='center')
    tasks_count = int(str(center.findAll('p')[1])[20:22])
    tasks_table = center.find('table', class_='vartopic')
    tasks = tasks_table.findAll('tr')[::2]
    answers = tasks_table.findAll('tr')[1::2]
    img_addresses = []
    excel_addresses = []
    word_addresses = []
    for i in range(len(tasks)):
        tasks[i] = tasks[i].find('td', class_='topicview')
        tasks[i] = tasks[i].find('script')

    print(tasks)
    # making img_addresses list
    for i in range(len(tasks)):
        txt = str(tasks[i])
        if 'img' in txt:
            ind = txt.find('img') + 9
            ind1 = 0
            for j in range(ind, len(txt)):
                if txt[j] == '"':
                    ind1 = j
                    break
            img_addresses.append(txt[ind:ind1])
        else:
            img_addresses.append(None)

    # making answers list
    for i in range(len(answers)):
        answers[i] = answers[i].find('script')
        script_txt = str(answers[i])
        left_border_index = script_txt.find("'") + 1
        right_border_index = script_txt.rfind("'")
        answers[i] = [script_txt[left_border_index:right_border_index]]


    # making excel_files list
    for i in range(len(tasks)):
        txt = str(tasks[i])
        if '<a' in txt and 'xls' in txt:
            ind = txt.find('<a') + 9
            ind1 = 0
            for j in range(ind, len(txt)):
                if txt[j] == '"':
                    ind1 = j
                    break
            excel_addresses.append(txt[ind:ind1])
        else:
            excel_addresses.append(None)
    # making word_files list
    for i in range(len(tasks)):
        txt = str(tasks[i])
        if '<a' in txt and 'docx' in txt:
            ind = txt.find('<a') + 9
            ind1 = 0
            for j in range(ind, len(txt)):
                if txt[j] == '"':
                    ind1 = j
                    break
            word_addresses.append(txt[ind:ind1])
        else:
            word_addresses.append(None)
    result_tasks = []
    import task_parsers
    for i in range(len(tasks)):
        result_tasks.append(task_parsers.get_all_tasks(tasks[i]))

    for i in range(0, len(result_tasks)):
        flag = False
        dele = ''
        new_str = result_tasks[i]
        for j in range(len(result_tasks[i])):

            if result_tasks[i][j] == '<':
                flag = True

            if flag:
                dele += result_tasks[i][j]

            if result_tasks[i][j] == '>':
                flag = False
                if dele != "<sup>":
                    new_str = new_str.replace(dele, ' ')
                    dele = ''
                else:
                    new_str = new_str.replace(dele, '"')
                    dele = ''
        result_tasks[i] = new_str

    # for i in range(len(result_tasks)):
    #   print(result_tasks[i])

    num = random.randint(0, tasks_count - 1)
    return result_tasks[num], answers[num], img_addresses[num], excel_addresses[num], word_addresses[num]
