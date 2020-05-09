import db

if __name__ == "__main__":
    test = db.database()
    print(test.barchart('someday', '2020-03-20'))