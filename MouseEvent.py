class MouseEvent:
    event_types = {512: "Mouse Move",
                513: "Left Mouse Down",
                514: "Left Mouse Up"}


    def __init__(self, event_type):
        #print("wut" + str(event_type))
        self.event_type = self.event_types.get(event_type)
        #self.name = name

    def __repr__(self):
        return 'MouseEvent: {}'.format(self.event_type)
