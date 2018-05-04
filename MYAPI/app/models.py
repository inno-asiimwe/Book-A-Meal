USERS = [{'id':1, 'email':'ronald@gmail.com', 'password':'123456', 'authenticated':False},
            {'id':2, 'email':'mutebi@gmail.com', 'password':'123hdg', 'authenticated':True}]



class User():
    def __init__ (self, email , password):
        self.email = email
        self.password = password
        

    def login_user(self, email, password, password2):
        """This represents a sign/login in"""
        user = [x for x in USERS if x.get('email') ==email ]
        if password == password2:
            user = {'email': email, 'password':password}
            return "You have registered successfully"

        if user:
            return user[0]
        return None

    def register_user(self, new_user):
        """This represents a user registration"""
        for x in USERS:
            user = [x for x in USERS if x.get('email') == new_user['email'] ]
            if len(user)>0:
                return "This email already exists"
            else:
                USERS.append(new_user[0])
                return "You have successfully registered"

                
           


    


ORDERS = [{'order_id':3, 'user_id':'id', 'meal':'meal_name'}]


class Order():


    def get_orders(self):
        all_orders = [ d for d in ORDERS ]
        return all_orders

MENUS = [{'day': 'Monday', 'menu':[{'meal_name':'Kikomando', 'price':1700, 'user_id':'id'},
    {'meal_name':'Posho and chicken', 'price':3400, 'user_id':'id'}] }]


class Menu():

    
    def save(self, day, menu):
        MENUS.append( { 'day': day, 'menu':menu } )



MEALS =[{'meal_name':'Kikomando', 'price':1700, 'user_id':'id'},
        {'meal_name':'Posho and chicken', 'price':3400, 'user_id':'id'}]



class Meal():
    meal = [{'meal_name':'Beef with rice', 'price':3000}, {'meal_name':'Minced goat meet', 'price':7000}]
    def save_meal(self, meal):
        for x in MEALS:
            if x['meal_name'] ==meal['meal_name']:
                return "The meal is already Present"
            else:
                MEALS.append(meal)
            return "The meal is now in the menu"

        

    def get_all_meals(self):
        return MEALS

            




