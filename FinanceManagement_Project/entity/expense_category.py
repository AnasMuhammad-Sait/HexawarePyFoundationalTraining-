class ExpenseCategory:
    def __init__(self, category_id=None, category_name=''):
        self.__category_id = category_id
        self.__category_name = category_name

    def get_category_id(self):
        return(self.__category_id)

    def get_category_name(self):
        return(self.__category_name)

    def set_category_id(self, category_id):
        self.__category_id = category_id

    def set_category_name(self, category_name):
        self.__category_name = category_name
