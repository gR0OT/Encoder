import argparse
from math import floor
import wolframalpha as wf
import sys

"""
Create translate dictionary
00-25 lowercase
26-51 uppercase
52-61 numbers
62-83 special chars
"""
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
specials = " !@#$%^&*()_+;:\'\"\\|/.,<>\{\}[]`~"

translate_dict = {}

for i, char in enumerate(list(specials)):
    translate_dict[char] = '{:02d}'.format(i)

for i, char in enumerate(list(lowercase)):
    translate_dict[char] = '{:02d}'.format(i + len(specials))

for i, char in enumerate(list(uppercase)):
    translate_dict[char] = '{:02d}'.format(i + len(specials) + len(lowercase))

for i, char in enumerate(list(numbers)):
    translate_dict[char] = '{:02d}'.format(i + len(specials) + len(lowercase) + len(uppercase))

app_id = "35VRHE-6KRPH82ALH"
client = wf.Client(app_id)

def translate_str2num(input: str) -> str:
    output = []
    for char in input:
        trans_char = translate_dict[char]
        output.append(trans_char)
    
    output = "".join(output)
    return output

def translate_num2str(input: list) -> str:
    output = []
    for char in input:
        trans_char = next((k for k, v in translate_dict.items() if v == char), char)
        output.append(trans_char)
        
    output = "".join(output)
    return output

def encode(message: str) -> str:
    # add trailing spaces, wolfram creates fractions with rounding last digit even if told not to do so
    message = message + " "*7
    message_len = len(message)
    # encode message to number
    enc_message = translate_str2num(message)
    
    # get fraction representation of the number (using wolfram)
    question = f"convert {message_len}.{enc_message} to fraction"
    print(question)
    res = client.query(question)
    ans = next(res.results).text
    return ans

def decode(frac: str) -> str:
    a,b = frac.split('/')
    a,b = int(a), int(b)
    message_len = floor(a/b)
    question = f"({str(a)}/{str(b)}) - {message_len} to 2000 decimal places"

    res = client.query(question)
    decimal_number = next(res.results).text
    enc_message = []
    
    for i in range(0, len(decimal_number), 2):
        if i == 0: continue
        enc_message.append(decimal_number[i:i + 2])
        if len(enc_message) == message_len: break

    message = translate_num2str(enc_message)

    return message

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    #TODO add parser groups for encode and decode
    parser.add_argument_group()

    # encode/decode option, only one can be specified
    action = parser.add_mutually_exclusive_group()
    action.add_argument('-e', '--encode', action='store_true', help='Encode message to fraction')
    action.add_argument('-d', '--decode', action='store_true', help='Decode message from fraction')
    
    parser.add_argument('-m', '--message', help='Message to encode')
    parser.add_argument('-f', '--fraction', type=str, help='Fraction to decode (a/b), e.g. 1234/5678')

    # parse arguments, if no args specified print help
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.encode:
        if args.message:
            encoded_message = encode(args.message)
            print(f"Encoded message: {encoded_message}")
        else:
            parser.error("--message is required when encoding")

    elif args.decode:
        if args.fraction:
            decoded_message = decode(args.fraction)
            print(f"Decoded message: {decoded_message}")
        else:
            parser.error("--fraction is required when decoding")

