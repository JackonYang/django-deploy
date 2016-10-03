# -*- Encoding: utf-8 -*-
import argparse


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

    return {
        'project_root': project_root,
        'project_name': project_name,
    }


if __name__ == '__main__':
    print(parse_args())
