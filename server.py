from flask import Flask, render_template, request, redirect, abort
import os
import knowledge_graph
import json
app = Flask(__name__)

component_path = './templates/components/'
title = 'MoocData'
header = ''
challenge_names = ['kdd-cup-2015', 'mooccube-2020']
challenges = {}
copy_right = ''
publication_contents = ['pubs-2020', 'pubs-2019', 'pubs-2018', 'pubs-2017', 'pubs-2016', 'invited-talks']
publications = {}
data = {}
data_names = ['xiaomu-question', 'concept-extraction', 'prerequisite-relation', 'user-activity', 'course-recommendation', 'MOOCCube']

def preload():
    global header, challenges, data, publications, copy_right
    with open(component_path + 'header.html', 'r', encoding='utf-8') as f:
        header = f.read()
    for name in challenge_names:
        file_path = component_path + 'challenges/' + name + '.html'
        with open(file_path, 'r', encoding='utf-8') as f:
            challenges[name] = f.read()
    for name in data_names:
        file_path = component_path + 'data/' + name + '.html'
        with open(file_path, 'r', encoding='utf-8') as f:
            data[name] = f.read()
    with open(component_path + 'copyright.html', 'r', encoding='utf-8') as f:
        copy_right = f.read()
    for content in publication_contents:
        file_path = component_path + 'publications/' + content + '.html'
        with open(file_path, 'r', encoding='utf-8') as f:
            publications[content] = f.read()


@app.route('/')
def main_page():
    return render_template('main_page.html', title=title, header=header, copyright=copy_right)


@app.route('/data')
def data_default_page():
    return redirect('/data/'+data_names[0])

@app.route('/data/<data_name>')
def data_page(data_name):
    if data_name not in data_names:
        return
    return render_template('data_page.html', title=title, header=header, copyright=copy_right, data=data[data_name])


@app.route('/about')
def about_page():
    return render_template('about_page.html', title=title, header=header, copyright=copy_right)


@app.route('/publications')
def publication_page():
    return render_template('publication_page.html', title=title, header=header, copyright=copy_right, publications=publications)


@app.route('/challenges')
def challenge_default_page():
    return redirect('/challenges/' + challenge_names[0])


@app.route('/challenges/<challenge_name>')
def challenge_page(challenge_name):
    if challenge_name not in challenge_names:
        return
    return render_template('challenge_page.html', title=title, header=header, challenge=challenges[challenge_name], copyright=copy_right)

'''
@app.route('/download_data/<file_name>')
def download_data(file_name):
    print('download data:', file_name)
    # if not re.match(r'^([a-z0-9]+/)*([a-z0-9]+\.?)+$', file_path):
    #    return
    file_lists = os.listdir('./static/data')
    if file_name in file_lists:
        return app.send_static_file('data/' + file_name)
    else:
        return


@app.route('/download_publication/<file_name>')
def download_publication(file_name):
    print('download publication:', file_name)
    # if not re.match(r'^([a-z0-9]+/)*([a-z0-9]+\.?)+$', file_path):
    #    return
    file_lists = os.listdir('./static/publications')
    if file_name in file_lists:
        return app.send_static_file('publications/' + file_name)
    else:
        return
'''

@app.route('/mooc_knowledge_graph')
def default_mooc_knowledge_graph():
    return redirect('/mooc_knowledge_graph/MOOC Knowledge Graph')

@app.route('/mooc_knowledge_graph/<field>')
def mooc_knowledge_graph(field):
    info = knowledge_graph.load_info(field)
    if info is None:
        abort(404)
    return render_template('mooc_knowledge_graph_page.html', title='MOOC Knowledge Graph', info=info, copyright=copy_right)

@app.route('/mooc_knowledge_graph/get_data/<field>')
def get_field_data(field):
    res = knowledge_graph.load_data(field)
    if res is None:
        abort(400)
    return json.dumps(res, ensure_ascii=False)

@app.route('/test')
def test():
    with open('flare.json', 'r', encoding='utf-8') as f:
        res = f.read()
    return res

preload()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9123)
    # only at Linux server can run following command to start service
    # gunicorn server:app -k gevent --worker-connections 4 -b 0.0.0.0:9123
