class DateAndTime:
    def date():
        #Scrive la data attuale
        import datetime
        now = datetime.datetime.now()
        print(now.strftime("%d/%m/%Y"))

    def time():
        #Scrive l'ora attuale
        import datetime
        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S"))