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
    name = data['name']
    city = data['city']
    rating = data['rating']
    price = data['price']
    query = "UPDATE hotels SET name = %s, city = %s, price = %s WHERE hotel_id = %s"
    values = (name, city, rating, price, hotel_id)
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
@app.route('/booking', methods=['POST'])
def add_booking():
    data = request.get_json()
    hotel_id = data['hotel_id']
    name = data['name']
    email = data['email']
    phone = data['phone']
    checkin_date = data['checkin_date']
    checkout_date = data['checkout_date']
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
