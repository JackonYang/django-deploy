# -*- Encoding: utf-8 -*-
import argparse
import codecs
import os
import shutil

from jinja2 import Environment, FileSystemLoader


TMPL_DIR = './etc-tmpl'

env = Environment(loader=FileSystemLoader(TMPL_DIR))


def gen_render_list(etc_root):
    for dirpath, dirnames, files in os.walk(TMPL_DIR):
        relpath = os.path.relpath(dirpath, TMPL_DIR)
        if relpath != '.':
            # ensuer_etc_dir
            ensuer_dir(os.path.join(etc_root, relpath))
        for f in files:
            if not f.startswith('.'):
                f = os.path.join(relpath, f)
                yield f, os.path.join(etc_root, f)


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


def ensuer_etc_dir(etc_root):
    if os.path.exists(etc_root):
        shutil.rmtree(etc_root)
    ensuer_dir(etc_root)


def ensuer_var_dir(var_root):
    # no remove
    ensuer_dir(var_root)
    ensuer_dir(os.path.join(var_root, 'socket'))
    ensuer_dir(os.path.join(var_root, 'log'))


def render(options):

    etc_root = options['etc_root']
    ensuer_etc_dir(etc_root)

    var_root = options['var_root']
    ensuer_var_dir(var_root)

    for i, o in gen_render_list(etc_root):
        template = env.get_template(i)
        with codecs.open(o, 'w', 'utf8') as f:
            f.write(template.render(**options))


def parse_args():
    parser = argparse.ArgumentParser(
        prog='django-deploy',
        usage='python gen.py [options] path/to/django/project/',
        description='generate etc files for deploying'
    )

    parser.add_argument('project_path', type=str,
                        help='path of target project')
    parser.add_argument('-d', '--domain', default='jackon.me',
                        help='domain name')
    parser.add_argument('-e', '--etc', default='deploy_etc',
                        help='path of deploy etc')
    parser.add_argument('-p', '--var', default='var',
                        help='path of var files')
    parser.add_argument('-n', '--process_num', default='4',
                        help='maximum number of uwsgi worker processes')

    args = parser.parse_args()

    # make sure that every path is abspath without '/' suffix
    project_root = os.path.abspath(args.project_path).rstrip('/')
    etc_root = os.path.abspath(args.etc).rstrip('/')
    var_root = os.path.abspath(args.var).rstrip('/')

    django_root = os.path.abspath(find_django_root(project_root)).rstrip('/')
    if not django_root:
        raise ValueError('django_root not found in %s' % project_root)

    project_name = project_root.rstrip('/').split('/')[-1]

    return {
        'project_root': project_root,
        'project_name': project_name,
        'django_root': django_root,
        'etc_root': etc_root,
        'var_root': var_root,
        'settings': find_settings(django_root, project_name),
        'domain': args.domain,
        'process_num': args.process_num,
        # static and media files
        'static_root': os.path.abspath(os.path.join(django_root, 'static')),
        'media_root': os.path.abspath(os.path.join(django_root, 'media')),
        # socket files
        'django_socket_file': 'socket/django_%s.sock' % project_name
    }


if __name__ == '__main__':
    options = parse_args()

    print '-' * 20, ' options ', '-' * 20
    for k, v in options.items():
        print '%s: %s' % (k, v)
    print '-' * 49

    render(options)
