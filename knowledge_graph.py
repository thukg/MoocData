import os
import json

prev = './knowledge_graph_data/'
info = {}

def get_concept_number(data):
    return len(data.split('"name"')) - 1

def preload():
    global info
    with open(prev + 'basic_info.json', 'r', encoding='utf-8') as f:
        tmp = f.read().split('\n')
        for line in tmp:
            if line == '':
                continue
            a = json.loads(line)
            info[a['field']] = a
    with open(prev + 'data.json', 'r', encoding='utf-8') as f:
        tmp = f.read().split('\n')
        for line in tmp:
            if line == '':
                continue
            a = json.loads(line)
            field = a['name']
            info[field]['data'] = a
            info[field]['concept-number'] = get_concept_number(line)

def load_info(field):
    if field not in info:
        return None
    res = {}
    res['title'] = field
    pre = info[field]
    if 'data' not in pre:
        file = prev + 'data/' + field + '.json'
        if not os.path.exists(file):
            return None
        with open(file, 'r', encoding='utf-8') as f:
            raw = f.read()
            data = json.loads(raw)
            pre['data'] = data
    if 'intro' not in pre:
        file = prev + 'intro/'+ field + '.html'
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
        else:
            code = ''
        text = []
        text.append('当前为{}级领域'.format(len(pre['routes'])))
        if len(pre['routes']) > 0:
            fa = pre['routes'][0]
            text.append('上位领域：<a href="/mooc_knowledge_graph/{}">{}</a>'.format(fa, fa))
        if len(pre['subfields']) > 0:
            text.append('直接子领域有{}个，二级子领域有{}个'.format(len(pre['subfields']), pre['grand_son_number']))
        text.append('包含领域/概念总数{}个'.format(pre['all_son_number']))
        text = '<hr /><p><b>当前领域的信息：</b> <br /> 本领域为 {} <br /> {}</p>'.format(field, '<br />'.join(text))
        pre['intro'] = code + text
    res['intro'] = pre['intro']
    if len(pre['subfields']) > 0:
        hint = '' if field != 'MOOC Knowledge Graph' else '（灰色为未标注）'
        html = '<hr /><div id="buttons"><p><b>下位领域{}：</b></p>'.format(hint)
        for button in pre['subfields']:
            labeled = False if button not in info else info[button]['is_labeled']
            labeled = 'btn-success' if labeled else 'btn-light'
            html += '<a href="/mooc_knowledge_graph/{}"><button type="button" class="btn {} my-button">{}</button></a>'.format(button, labeled, button)
        html += '</div>'
    else:
        html = ''
    res['buttons_html'] = html
    return res

def load_data(field):
    global info
    if field not in info or 'data' not in info[field]:
        return None
    return info[field]['data']

preload()