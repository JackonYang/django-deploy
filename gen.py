# -*- Encoding: utf-8 -*-
import argparse
import codecs
import os
import shutil

from jinja2 import Environment, FileSystemLoader


TMPL_DIR = './etc-tmpl'

env = Environment(loader=FileSystemLoader(TMPL_DIR))


def get_render_list(options):
    deploy_root = options['deploy_root']
    if os.path.exists(deploy_root):
        shutil.rmtree(deploy_root)
    ensuer_dir(deploy_root)

    for dirpath, dirnames, files in os.walk(TMPL_DIR):
        relpath = os.path.relpath(dirpath, TMPL_DIR)
        if relpath != '.':
            ensuer_dir(os.path.join(deploy_root, relpath))
        for f in files:
            if not f.startswith('.'):
                f = os.path.join(relpath, f)
                yield f, os.path.join(deploy_root, f)


def find_settings(django_root, project_name, basename='settings'):
    normalize_name = project_name.replace('-', '_')

    settings_dirs = [
        'base',
        normalize_name,
        project_name,
    ]
    settings_dirs.extend(normalize_name.split('_'))

    for item in settings_dirs:
        target = os.path.join(django_root, item, '%s.py' % basename)
        if os.path.exists(target):
            return '%s.%s' % (item, basename)

    raise ValueError('settings.py not found. django_root=%s' % django_root)


def find_django_root(project_root, key='manage.py'):
    for dirpath, dirnames, files in os.walk(project_root):
        if key in files:
            return dirpath


def ensuer_dir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    return path_name


def render(options):
    for i, o in get_render_list(options):
        template = env.get_template(i)
        with codecs.open(o, 'w', 'utf8') as f:
            f.write(template.render(**options))


def parse_args():
    parser = argparse.ArgumentParser(
        prog='django-deploy',
        usage='./gen.py',
        description='1 key to deploy django production server.'
    )

    parser.add_argument('project', type=str,
                        help='path of target project')
    parser.add_argument('-o', '--output', default='deploy',
                        help='path of output')
    parser.add_argument('-n', '--process_num', default='4',
                        help='maximum number of uwsgi worker processes')

    args = parser.parse_args()

    deploy_root = args.output

    project_root = args.project
    project_name = project_root.rstrip('/').split('/')[-1]

    django_root = find_django_root(project_root)
    if not django_root:
        raise ValueError('django_root not found in %s' % project_root)

    return {
        'project_root': project_root,
        'project_name': project_name,
        'django_root': django_root,
        'deploy_root': deploy_root,
        'settings': find_settings(django_root, project_name),
        'wsgi_file': os.path.abspath(os.path.join(deploy_root, 'wsgi.py')),
        'process_num': args.process_num,
        'socket_file': os.path.abspath(os.path.join(deploy_root, '%s.sock' % project_name)),
    }


if __name__ == '__main__':
    options = parse_args()
    print(options)

    render(options)
