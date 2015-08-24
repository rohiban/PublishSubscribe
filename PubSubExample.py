__author__ = 'rbansal'

from pubsub import pub


class IRCTC(object):
    def __init__(self):
        self.dict = {1234:'train-1234', 3456:'train-3456', 5678:'train-5678', 7890:'train-7890'}

    def get_trains(self):
        return self.dict.keys()

    def get_train_topic(self, train_no):
        return self.dict.get(train_no)

    # construct a callable object, with some parameters
    def publish_availability(self):
        for (train_no, topic) in self.dict.items():
            pub.sendMessage(topic, train_no=train_no, no_of_seats=int(train_no/100))


class Passenger(object):
    def __init__(self, name, irctc):
        self.name = name
        self.booking_system = irctc

    def interested_in(self, train_no):
        pub.subscribe(self.availability_update, self.booking_system.get_train_topic(train_no))

    def availability_update(self, train_no, no_of_seats):
        print '    Availability for train # %d : %d' %(train_no, no_of_seats)



irctc = IRCTC()

rohit = Passenger('rohit', irctc)
rohit.interested_in(train_no=3456)

sunder = Passenger('sunder', irctc)
sunder.interested_in(train_no=5678)

print 'pub-sub example demonstration ->'

irctc.publish_availability()
