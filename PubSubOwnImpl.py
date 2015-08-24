__author__ = 'rbansal'

import inspect


class Subscriber(object):
    def __init__(self, topic, callable):
        self.topic = topic
        self.to_call = callable
        self.no_of_reqd_args = len(self.get_reqd_args(callable)) - 1  # for self

    def get_reqd_args(self, callable):
        args, varargs, varkw, defaults = inspect.getargspec(callable)
        if defaults:
            args = args[:-len(defaults)]
        return args

    def call_the_method(self, **kwargs):
        #print 'arguments are ====', kwargs

        if len(kwargs.keys()) == self.no_of_reqd_args:
            return self.to_call(**kwargs)
        else:
            print 'callable NOT called, argument mismatch : expected - %d, got - %d' %(self.no_of_reqd_args, len(kwargs.keys()))


class myPublisher(object):
    def __init__(self):
        self.listener_dict = {}
        pass

    def subscribe(self, callable, topic_name):
        subscriber_list = self.listener_dict.get(topic_name)

        if subscriber_list is None:  # this topic is not registered yet
            subscriber_list = []
            subscriber_list.append(Subscriber(topic_name, callable))
            self.listener_dict.setdefault(topic_name, subscriber_list)
        else:  # topic is already registered, just add another subscriber
            subscriber_list.append(Subscriber(topic_name, callable))

    # return all the topics registered with the publisher
    def getTopics(self):
        return self.listener_dict.keys()

    # send message to subscribers of a given topic
    def sendMessage(self, topic, **kwargs):
        subscribers = self.listener_dict.get(topic)
        if subscribers is not None:
            for subscriber in subscribers:
                #dd = inspect.getcallargs(subscriber.to_call, **kwargs)
                #print dd
                subscriber.call_the_method(**kwargs)


pub = myPublisher()

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
