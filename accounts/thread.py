from threading import Thread

class EmailThread(Thread):
    def __init__(self,email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send()