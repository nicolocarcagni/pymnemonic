# Pymnemonic

Pymnemonic is a fun and interactive project that generates cryptographic mnemonic phrases using microphone noise as a source of entropy. The generated phrases can be used for secure password management and cryptocurrency wallets.

## How It Works

Pymnemonic captures random noise from your microphone and converts it into binary sequences. These sequences are then transformed into mnemonic phrases using the BIP-39 English Wordlist. The resulting phrases are both secure and memorable, providing a unique blend of security and entertainment.

## Usage

1. Install the required libraries using `pip`:
```bash
pip3 install -r requirements.txt
```

2.Run the script
```bash
python3 pymnemonic.py
```

3. Follow the on-screen instructions to generate your mnemonic phrase.

## Note

If the `english.txt` wordlist is missing, Pymnemonic will automatically download it from [here](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt).

## Contributors

- [nicolocarcagni](https://github.com/nicolocarcagni)

## License

This project is licensed under [GPL](LICENSE).
