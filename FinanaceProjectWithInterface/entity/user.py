class User:
    def __init__(self,user_id =None, username ='', password='',email=''):
        self.__user_id = user_id 
        self.__username = username 
        self.__password = password 
        self.__email = email
    
    def get_user_id(self):
        return(self.__user_id)

    def get_username(self):
        return(self.__username)
    
    def get_password(self):
        return(self.__password)
    
    def get_email(self):
        return(self.__email)
    
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email
