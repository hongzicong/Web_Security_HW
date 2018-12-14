# -*- coding: utf-8 -*-
import sys
import asn1
import binascii

tag_id_to_string_map = {
    asn1.Numbers.Boolean: "BOOLEAN",
    asn1.Numbers.Integer: "INTEGER",
    asn1.Numbers.BitString: "BIT STRING",
    asn1.Numbers.OctetString: "OCTET STRING",
    asn1.Numbers.Null: "NULL",
    asn1.Numbers.ObjectIdentifier: "OBJECT",
    asn1.Numbers.PrintableString: "PRINTABLESTRING",
    asn1.Numbers.IA5String: "IA5STRING",
    asn1.Numbers.UTCTime: "UTCTIME",
    asn1.Numbers.Enumerated: "ENUMERATED",
    asn1.Numbers.Sequence: "SEQUENCE",
    asn1.Numbers.Set: "SET"
}

class_id_to_string_map = {
    asn1.Classes.Universal: "U",
    asn1.Classes.Application: "A",
    asn1.Classes.Context: "C",
    asn1.Classes.Private: "P"
}

object_id_to_string_map = {
    "1.3.6.1.5.5.7.1.1": "authorityInfoAccess",

    "2.5.4.3": "commonName",
    "2.5.4.4": "surname",
    "2.5.4.5": "serialNumber",
    "2.5.4.6": "countryName",
    "2.5.4.7": "localityName",
    "2.5.4.8": "stateOrProvinceName",
    "2.5.4.9": "streetAddress",
    "2.5.4.10": "organizationName",
    "2.5.4.11": "organizationalUnitName",
    "2.5.4.12": "title",
    "2.5.4.13": "description",
    "2.5.4.42": "givenName",

    "1.2.840.113549.1.9.1": "emailAddress",

    "2.5.29.14": "X509v3 Subject Key Identifier",
    "2.5.29.15": "X509v3 Key Usage",
    "2.5.29.16": "X509v3 Private Key Usage Period",
    "2.5.29.17": "X509v3 Subject Alternative Name",
    "2.5.29.18": "X509v3 Issuer Alternative Name",
    "2.5.29.19": "X509v3 Basic Constraints",
    "2.5.29.30": "X509v3 Name Constraints",
    "2.5.29.31": "X509v3 CRL Distribution Points",
    "2.5.29.32": "X509v3 Certificate Policies Extension",
    "2.5.29.33": "X509v3 Policy Mappings",
    "2.5.29.35": "X509v3 Authority Key Identifier",
    "2.5.29.36": "X509v3 Policy Constraints",
    "2.5.29.37": "X509v3 Extended Key Usage",

    # Algorithm
    '1.2.840.10040.4.1': 'DSA',
    "1.2.840.10040.4.3": "sha1DSA",
    "1.2.840.113549.1.1.1": "RSA",
    "1.2.840.113549.1.1.2": "md2RSA",
    "1.2.840.113549.1.1.3": "md4RSA",
    "1.2.840.113549.1.1.4": "md5RSA",
    "1.2.840.113549.1.1.5": "sha1RSA",
    '1.3.14.3.2.29': 'sha1RSA',
    '1.2.840.113549.1.1.13': 'sha512RSA',
    '1.2.840.113549.1.1.11': 'sha256RSA'
}

version_id_to_string_map = {
    0: 'V1',
    1: 'V2',
    2: 'V3'
}

time_id_to_string_map = {
    0: 'not before: ',
    1: 'not after: '
}


def tag_id_to_string(identifier):
    if identifier in tag_id_to_string_map:
        return tag_id_to_string_map[identifier]
    return '{:#02x}'.format(identifier)


def class_id_to_string(identifier):
    if identifier in class_id_to_string_map:
        return class_id_to_string_map[identifier]
    raise ValueError('Illegal class: {:#02x}'.format(identifier))


def object_identifier_to_string(identifier):
    if identifier in object_id_to_string_map:
        return object_id_to_string_map[identifier]
    return identifier


def value_to_string(tag_number, value):
    if tag_number == asn1.Numbers.ObjectIdentifier:
        return object_identifier_to_string(value)
    elif isinstance(value, bytes):
        return binascii.hexlify(value).upper().decode()
    elif isinstance(value, str):
        return value
    else:
        return repr(value)


class X509Process:

    def __init__(self, file):
        self.file = file
        self.count = 2

    def process(self):
        encoded_bytes = file.read()
        decoder = asn1.Decoder()
        decoder.start(encoded_bytes)
        self.print_result(decoder)

    def print_result(self, input_stream, index=0):
        while not input_stream.eof():
            tag = input_stream.peek()
            if tag.typ == asn1.Types.Primitive:
                tag, value = input_stream.read()
                if self.count == 2:
                    print("VERSION: {}".format(version_id_to_string_map[value]))
                    self.count -= 1
                elif self.count == 1:
                    print("SERIAL NUMBER: {}".format(value))
                    self.count -= 1
                elif tag_id_to_string(tag.nr) == "OBJECT":
                    print('{}: '.format(value_to_string(tag.nr, value)), end='')
                elif tag_id_to_string(tag.nr) == "PRINTABLESTRING":
                    print(value_to_string(tag.nr, value))
                else:
                    print('[{}] {}: {}'.format(class_id_to_string(tag.cls), tag_id_to_string(tag.nr), value_to_string(tag.nr, value)))
            elif tag.typ == asn1.Types.Constructed:
                input_stream.enter()
                self.print_result(input_stream, index + 2)
                input_stream.leave()


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, "rb") as file:
        x509process = X509Process(file)
        x509process.process()
