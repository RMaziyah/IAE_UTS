from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1202201389",
  database="hotel"
)
cursor = db.cursor()

# add hotel endpoint
@app.route('/hotels', methods=['POST'])
def add_hotel():
    data = request.get_json()
    name = data['name']
    city = data['city']
    rating = data['rating']
    price = data['price']
    query = "INSERT INTO hotels (name, city, rating, price) VALUES (%s, %s, %s, %s)"
    values = (name, city, rating, price)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Hotel added successfully'})

# update hotel endpoint
@app.route('/hotels/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    rating = data.get('rating')
    price = data.get('price')
    query = "UPDATE hotels SET "
    sets = []
    values = []
    if name:
        sets.append("name = %s")
        values.append(name)
    if city:
        sets.append("city = %s")
        values.append(city)
    if rating:
        sets.append("rating = %s")
        values.append(rating)
    if price:
        sets.append("price = %s")
        values.append(price)
    query += ", ".join(sets)
    query += " WHERE hotel_id = %s"
    values.append(hotel_id)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Hotel updated successfully'})

# delete hotel endpoint
@app.route('/hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    query = "DELETE FROM hotels WHERE hotel_id = %s"
    values = (hotel_id,)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Hotel deleted successfully'})

# get hotels endpoint
@app.route('/hotels', methods=['GET'])
def get_hotels():
    query = "SELECT * FROM hotels ORDER BY city, rating;"
    cursor.execute(query)
    result = cursor.fetchall()
    hotels = []
    for hotel in result:
        hotel_data = {}
        hotel_data['name'] = hotel[1]
        hotel_data['city'] = hotel[2]
        hotel_data['price'] = hotel[4]
        hotel_data['rating'] = hotel[3]
        hotels.append(hotel_data)
    return jsonify({'hotels': hotels})

# get hotel based on city endpoint
@app.route('/hotels/<string:city>', methods=['GET'])
def get_hotels_by_city(city):
    query = "SELECT * FROM hotels WHERE city = %s ORDER BY rating DESC;"
    cursor.execute(query, (city,))
    result = cursor.fetchall()
    hotels = []
    for hotel in result:
        hotel_data = {}
        hotel_data['name'] = hotel[1]
        hotel_data['city'] = hotel[2]
        hotel_data['price'] = hotel[4]
        hotel_data['rating'] = hotel[3]
        hotels.append(hotel_data)
    return jsonify({'hotels': hotels})


# add booking API
@app.route('/bookings', methods=['POST'])
def add_booking():
    data = request.get_json()
    hotel_name = data['hotel_name']
    city = data['city']
    name = data['name']
    email = data['email']
    phone = data['phone']
    checkin_date = data['checkin_date']
    checkout_date = data['checkout_date']
    
    # Query to obtain hotel_id based on the given hotel name and city
    query = "SELECT hotel_id FROM hotels WHERE name = %s AND city = %s"
    values = (hotel_name, city)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        return jsonify({'message': 'Hotel not found'})
    
    # Insert the booking with the obtained hotel_id
    hotel_id = result[0]
    query = "INSERT INTO bookings (hotel_id, name, email, phone, checkin_date, checkout_date) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (hotel_id, name, email, phone, checkin_date, checkout_date)
    cursor.execute(query, values)
    db.commit()
    booking_id = cursor.lastrowid
    return jsonify({'message': f'Booking added successfully with booking id: {booking_id}'})

# get booking API
@app.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    query = "SELECT * FROM bookings WHERE booking_id = %s"
    values = (booking_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        return jsonify({'message': 'Booking not found'})
    booking = {}
    booking['booking_id'] = result[0]
    booking['hotel_id'] = result[1]
    booking['name'] = result[2]
    booking['email'] = result[3]
    booking['phone'] = result[4]
    booking['checkin_date'] = result[5].strftime('%Y-%m-%d')
    booking['checkout_date'] = result[6].strftime('%Y-%m-%d')
    return jsonify({'booking': booking})

if __name__ == '__main__':
    app.run(debug=True)
