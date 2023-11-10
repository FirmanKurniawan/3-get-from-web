import serial
import time
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    host="172.31.254.158",
    database="magnet",
    user="postgres",
    password="magnet"
)
cursor = conn.cursor()

ser_dmr = serial.Serial('COM4', 19200, timeout=1)

try:
    command = "S1"
    ser_dmr.write(command.encode('utf-8'))

    if command == 'S1':
        while True:
            data = ser_dmr.readline().decode('utf-8')
            # Pemeriksaan apakah data telah diterima
            if data:
                print("Data yang diterima:", data)

                # Parsing data yang diterima
                temperature, humidity = data.split()  # Memisahkan data dengan spasi

                # Mengonversi nilai ke float
                temperature = float(temperature)
                humidity = float(humidity)
                heat_index = float(20.0)

                # Mendapatkan waktu saat ini
                current_time = time.strftime('%Y-%m-%d %H:%M:%S+00')

                # Menyimpan data ke database
                insert_query = "INSERT INTO dht22_sensors (temperature, humidity, heat_index, time) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (temperature, humidity, heat_index, current_time))
                conn.commit()

                # Keluar dari loop setelah data disimpan
                break

except KeyboardInterrupt:
    pass
finally:
    ser_dmr.close()
    cursor.close()
    conn.close()