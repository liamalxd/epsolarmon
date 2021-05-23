#!/bin/python3

SERIAL_SERVER_IP = '172.16.0.1'
SERIAL_SERVER_PORT = 8088
CSV_FILE = 'solar.csv'

import time
CURRENT_TIME = time.strftime("%Y%m%d-%H%M%S")

def create_modbus_conn(server_ip, server_port):
    from pymodbus.client.sync import ModbusTcpClient
    from pymodbus.transaction import ModbusRtuFramer

    conn = None

    try:
        conn = ModbusTcpClient(host = SERIAL_SERVER_IP, port = SERIAL_SERVER_PORT, framer=ModbusRtuFramer)
    except Exception as e:
        print(e)

    return conn

def open_modbus_conn(client):
    client.connect()

def close_modbus_conn(client):
    client.close()

def read_data(client):
    results = {}
    result = client.read_input_registers(0x3100,16,unit=1)

    if hasattr(result, 'registers'):
        results['time']           = CURRENT_TIME
        results['solarvoltage']   = float(result.registers[0] / 100.0)
        results['solarcurrent']   = float(result.registers[1] / 100.0)
        results['solarpwrlow']    = float(result.registers[2] / 100.0)
        results['solarpwrhigh']   = float(result.registers[3] / 100.0)
        results['batteryvoltage'] = float(result.registers[4] / 100.0)
        results['chargecurrent']  = float(result.registers[5] / 100.0)
        results['chargepwrlow']   = float(result.registers[6] / 100.0)
        results['chargepwrhigh']  = float(result.registers[7] / 100.0)
        results['loadvoltage']    = float(result.registers[8] / 100.0)
        results['loadcurrent']    = float(result.registers[9] / 100.0)
        results['loadpower']      = float(result.registers[10] / 100.0)

    result = client.read_input_registers(0x311A,2,unit=1)

    if hasattr(result, 'registers'):
        results['batterypercentage'] = float(result.registers[0])

    result = client.read_input_registers(0x330C,2,unit=1)

    if hasattr(result, 'registers'):
        results['generatedenergytoday'] = float(result.registers[0] / 100.0)

    result = client.read_input_registers(0x330E,2,unit=1)

    if hasattr(result, 'registers'):
        results['generatedenergymonth'] = float(result.registers[0] / 100.0)

    result = client.read_input_registers(0x3310,2,unit=1)

    if hasattr(result, 'registers'):
        results['generatedenergyyear'] = float(result.registers[0] / 100.0)

    result = client.read_input_registers(0x3312,2,unit=1)

    if hasattr(result, 'registers'):
        results['generatedenergytotal'] = float(result.registers[0] / 100.0)

    return results

def create_csv(data_dict, csv_file_name):
    import csv

    with open(csv_file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, data_dict.keys())
        dict_writer.writeheader()
        dict_writer.writerows([data_dict]) 

def main():
    client = create_modbus_conn(SERIAL_SERVER_IP, SERIAL_SERVER_PORT)

    if client:
        open_modbus_conn(client)
        data = read_data(client)
        close_modbus_conn(client)

        if data:
            create_csv(data, CSV_FILE) 

if __name__ == "__main__":
    main()
