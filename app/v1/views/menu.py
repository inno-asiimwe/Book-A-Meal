@app.route("/api/v1/menu")
def get_menu():
    return Menu.get_menu()

@app.route("/api/v1/menu", methods=["POST"])
def setup_menu():
    data = request.data
    id = data['meal_id']
    if id:
        return Menu.setup_menu(id)