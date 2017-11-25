class KeykoardEvent(object):
    def __init__(self, event_type, name):
        self.event_type = event_type
        self.name = name

    def __repr__(self):
        return 'KeyboardEvent: {} {}'.format(self.name, self.event_type)
