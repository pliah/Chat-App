class Person:
    '''
    Class represent a person in the Chat - name, socket client and IP address.
    '''
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"

    def set_name(self, name):
        '''
        set the person name
        :param name: str
        :return: None
        '''
        self.name = name


