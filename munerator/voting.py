from CodernityDB.database import Database


def main(args):
    db = Database('db')
    if not db:
        db.create()
    else:
        db.open()

    for x in xrange(100):
        print db.insert(dict(x=x))

    for curr in db.all('id'):
        print curr

if __name__ == '__main__':
    main()