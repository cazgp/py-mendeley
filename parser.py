def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title='Subcommands')

    document = subparser.add_parser('document')
    document.add_argument('-a', '--author', help='author')
    document.add_argument('-y', '--year', help='year')
    document.add_argument('-t', '--title', help='title')
    document.set_defaults(namespace='document')

    folder = subparser.add_parser('folder')
    kinds = folder.add_mutually_exclusive_group(required=True)
    kinds.add_argument('--id', type=int, help='folder id in sqlite')
    kinds.add_argument('--name', help='folder name in Mendeley')
    folder.set_defaults(namespace='folder')

    return parser.parse_args()
