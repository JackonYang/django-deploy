# -*- Encoding: utf-8 -*-
import argparse
import os


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


def parse_args():
    parser = argparse.ArgumentParser(
        prog='django-deploy',
        usage='./gen.py',
        description='1 key to deploy django production server.'
    )

    parser.add_argument("project", type=str,
                        help="path of target project")

    args = parser.parse_args()

    project_root = args.project
    project_name = project_root.rstrip('/').split('/')[-1]

    django_root = find_django_root(project_root)
    if not django_root:
        raise ValueError('django_root not found in %s' % project_root)

    return {
        'project_root': project_root,
        'project_name': project_name,
        'django_root': django_root,
        'settings': find_settings(django_root, project_name),
    }


if __name__ == '__main__':
    options = parse_args()
    print(options)
