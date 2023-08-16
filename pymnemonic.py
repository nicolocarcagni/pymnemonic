import sounddevice as sd
import subprocess
import os
import requests

# ANSI color codes for terminal text color
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_RESET = '\033[0m'

# URL of the BIP-39 English Wordlist
WORDLIST_URL = 'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt'

def generate_entropy_microphone(sample_rate, bits_to_generate, threshold=0.01):
    sd.default.samplerate = sample_rate
    sd.default.channels = 1  # Mono audio

    print("Generating binary entropy from microphone...")

    def callback(indata, frames, time, status):
        nonlocal bits_generated
        
        if any(indata > threshold) or any(indata < -threshold):
            bit = 1 if indata[0] > 0 else 0
            entropy_source.append(bit)
            bits_generated += 1

    entropy_source = []
    bits_generated = 0

    with sd.InputStream(callback=callback):
        while bits_generated < bits_to_generate:
            pass

    return entropy_source

def calculate_bip39_checksum(hex_checksum):
    # Get the first two hexadecimal digits
    hex_digits = hex_checksum[:2]

    # Convert the hexadecimal digits to binary
    binary_checksum = format(int(hex_digits, 16), '08b')

    return binary_checksum

def split_into_groups(binary_string, group_size):
    return [binary_string[i:i+group_size] for i in range(0, len(binary_string), group_size)]

def binary_group_to_decimal(binary_group):
    return int(binary_group, 2)

def download_wordlist(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def get_english_word(index, wordlist):
    return wordlist[index].strip()

if __name__ == "__main__":
    sample_rate = 44100  # Sample rate in Hz
    bits_to_generate = 256  # Number of bits to generate
    wordlist_file = 'english.txt'

    if not os.path.exists(wordlist_file):
        print("Downloading BIP-39 English Wordlist...")
        download_wordlist(WORDLIST_URL, wordlist_file)

    with open(wordlist_file, 'r') as f:
        wordlist = f.readlines()

    entropy_data = generate_entropy_microphone(sample_rate, bits_to_generate)

    # Limit generated values to a maximum of 256 (0-255)
    limited_entropy_data = [value % 256 for value in entropy_data]

    print(f"\n{COLOR_GREEN}Binary Entropy Generated:{COLOR_RESET}")
    for value in limited_entropy_data:
        print(value, end='')
    
    print(f"\n{COLOR_GREEN}Number of Generated Bits:{COLOR_RESET}", len(limited_entropy_data))
    
    # Convert bit list to a bit string (e.g., "011010101...")
    bit_string = ''.join(str(bit) for bit in limited_entropy_data)
    
    # Execute the terminal echo command and calculate SHASUM
    try:
        cmd = f'echo {bit_string} | shasum -a 256 -0'
        cmd_output = subprocess.check_output(cmd, shell=True, text=True)
        shasum = cmd_output.split()[0]
        print(f"\n{COLOR_GREEN}SHASUM:{COLOR_RESET}", shasum)

        # Calculate BIP39 checksum for the 24th word
        bip39_checksum = calculate_bip39_checksum(shasum)
        print(f"\n{COLOR_GREEN}BIP39 Checksum:{COLOR_RESET}", bip39_checksum)

        # Combine input and checksum, and split into groups of 11 bits
        combined_hash = bit_string + bip39_checksum
        hash_groups = split_into_groups(combined_hash, 11)
        print(f"\n{COLOR_GREEN}Combined Hash (11-bit groups):{COLOR_RESET}")
        for group in hash_groups:
            print(group, end=' ')

        # Convert each group to decimal and print
        decimal_groups = [binary_group_to_decimal(group) for group in hash_groups]
        print(f"\n{COLOR_GREEN}Decimal Conversion of Hash Groups:{COLOR_RESET}")
        for decimal_value in decimal_groups:
            print(decimal_value, end=' ')

        # Get English word for each decimal group
        mnemonic_phrase = [get_english_word(decimal_value, wordlist) for decimal_value in decimal_groups]
        print(f"\n{COLOR_GREEN}Mnemonic Phrase (24 Words):{COLOR_RESET}")
        print(' '.join(mnemonic_phrase))

    except subprocess.CalledProcessError as e:
        print(f"\n{COLOR_RED}Error while calculating SHASUM:{COLOR_RESET}", e)
