from fastapi import FastAPI, HTTPException

app = FastAPI()

# Mock data: List of guns stored as tuples (id, name, caliber, type, price)
guns_db = [
    (1, "Glock 19", "9mm", "Pistol", 500),
    (2, "Remington 870", "12 gauge", "Shotgun", 350),
    (3, "AR-15", "5.56mm", "Rifle", 1200),
]

@app.get("/")
def read_root():
    return "Welcome to the Gun Shop API! Use /guns to list available firearms or /guns/{id}/price for pricing."

@app.get("/guns")
def list_guns():
    """
    List all available guns.
    """
    return [
        f"ID: {gun[0]}, Name: {gun[1]}, Caliber: {gun[2]}, Type: {gun[3]}, Price: ${gun[4]:,.2f}"
        for gun in guns_db
    ]

@app.get("/guns/{gun_id}/price")
def get_gun_price(gun_id: int):
    """
    Get the price of a specific gun by ID.
    """
    for gun in guns_db:
        if gun[0] == gun_id:
            return f"The price of {gun[1]} ({gun[3]}, {gun[2]}) is ${gun[4]:,.2f}."
    raise HTTPException(status_code=404, detail="Gun not found")

@app.get("/guns/add")
def add_gun(id: int, name: str, caliber: str, type: str, price: float):
    """
    Add a new gun to the list using query parameters.
    """
    if any(gun[0] == id for gun in guns_db):
        raise HTTPException(status_code=400, detail="Gun with this ID already exists.")
    guns_db.append((id, name, caliber, type, price))
    return f"Gun {name} ({type}, {caliber}) added successfully with ID {id}."

@app.get("/guns/delete/{gun_id}")
def delete_gun(gun_id: int):
    """
    Delete a gun from the list by its ID.
    """
    for gun in guns_db:
        if gun[0] == gun_id:
            guns_db.remove(gun)
            return f"Gun with ID {gun_id} deleted successfully."
    raise HTTPException(status_code=404, detail="Gun not found")
