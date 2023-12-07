#!/bin/python3
import numpy as np

HEADER_FIELDS_COUNT = 9
KEY_VALUE_SEPARATOR = ":"
FIELD_SEPARATOR = ";"
CAEN_ADC_BITS = 14
CAEN_SAMPLING_PERIOD_SECONDS = 2e-9


class HeaderField:
    RECORD_LENGTH = "RecordLength"
    BOARD_ID = "BoardID"
    CHANNEL = "Channel"
    EVENT_NUMBER = "EventNumber"
    PATTERN = "Pattern"
    TRIGGER_TIMESTAMP = "TriggerTimeStamp"
    DC_OFFSET = "DCOffset(DAC)"
    PULSE_POLARITY = "PulsePolarity"
    INPUT_DYNAMIC_RANGE = "InputDynamicRange(Vpp)"


def _parse_header(file):
    header_text = ""

    if file.mode == "rb":
        field_separator_count = 0
        while True:
            character = file.read(1).decode()

            if character == '':
                raise EOFError

            if character == FIELD_SEPARATOR:
                field_separator_count += 1

            if field_separator_count == HEADER_FIELDS_COUNT:
                break

            header_text += character
        data = header_text.split(FIELD_SEPARATOR)
    elif file.mode == "r" or file.mode == "rt" or file.mode == "tr":
        raise Exception("Ascii file format not supported")
        # header_text += file.readline().rstrip("\n")
        # data = header_text.split(FIELD_SEPARATOR)[:-1]
    else:
        raise Exception("Wrong file open mode.")

    header = {}
    for field in data:
        field_split = field.split(KEY_VALUE_SEPARATOR)
        header[field_split[0]] = field_split[1]

    header[HeaderField.RECORD_LENGTH] = int(header[HeaderField.RECORD_LENGTH])
    header[HeaderField.BOARD_ID] = int(header[HeaderField.BOARD_ID])
    header[HeaderField.CHANNEL] = int(header[HeaderField.CHANNEL])
    header[HeaderField.EVENT_NUMBER] = int(header[HeaderField.EVENT_NUMBER])
    header[HeaderField.PATTERN] = int(
        header[HeaderField.PATTERN][2:], base=16) >> 2
    header[HeaderField.TRIGGER_TIMESTAMP] = int(
        header[HeaderField.TRIGGER_TIMESTAMP])
    header[HeaderField.DC_OFFSET] = int(
        header[HeaderField.DC_OFFSET][2:], base=16) >> 2
    header[HeaderField.PULSE_POLARITY] = 1 if header[HeaderField.PULSE_POLARITY] == "Positive" else 0
    header[HeaderField.INPUT_DYNAMIC_RANGE] = float(
        header[HeaderField.INPUT_DYNAMIC_RANGE])

    return header


def _parse_raw_data(file, record_length):
    wave_data = np.array((), dtype=np.int16)

    if file.mode == "rb":
        for i in range(record_length):
            value = int.from_bytes(file.read(2), byteorder="little")
            wave_data = np.append(wave_data, value)
        file.read(1)
    elif file.mode == "r" or file.mode == "rt" or file.mode == "tr":
        for i in range(record_length):
            value = int(file.readline()[:-1])
            wave_ascii = np.append(wave_ascii, value)
    else:
        raise Exception("Wrong file open mode.")

    return wave_data


def _convert_raw_data_to_voltage(header, raw_data):
    dc_offset = header[HeaderField.DC_OFFSET]
    dynamic_range = header[HeaderField.INPUT_DYNAMIC_RANGE]
    scale_factor = (2**CAEN_ADC_BITS)/dynamic_range

    return np.array((raw_data - dc_offset)/scale_factor, dtype=np.float32)


def read_wave_batch(file):
    waves = []
    while True:
        try:
            header = _parse_header(file)
            raw_data = _parse_raw_data(file, header[HeaderField.RECORD_LENGTH])
            time_array = np.arange(0, header[HeaderField.RECORD_LENGTH] *
                                   CAEN_SAMPLING_PERIOD_SECONDS, CAEN_SAMPLING_PERIOD_SECONDS, dtype=np.float64)
            voltage_data = _convert_raw_data_to_voltage(header, raw_data)
            wave = np.array((time_array, voltage_data))
            waves.append(wave)

        except EOFError:
            break

    return waves