from wavedump_data_reader import _parse_header, _parse_raw_data

with open("output_data/1712790865-CH0.dat", "rb") as f:
    linea = 1
    while True:
        print("******", linea)
        header = _parse_header(f)
        print(header)
        _parse_raw_data(f, header["RecordLength"])
        linea += 1