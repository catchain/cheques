# Description

This is a smart-contract for TON blockchain implementing service for managing cheques made by CAT. Cheques service provides a way for users to create a cheque for specific amount of Grams with associated key. It was made as a part of Telegram contest.

Assume Alice is the person who keeps Grams.

Alice generates random key and creates cheque for specific amount of grams  associated with generated key and send it to service. Then Alice can send key of created cheque to some random Bob. Bob activates cheque with given key and recieves grams to his wallet.

There is also another way of interacting with provided service. Bob generates key and sends hash of this key to Alice. Alice creates cheque identified by recieved hash and sends it to service contract. Than Bob activates cheque by generated key. This way prevents that Alice can activate cheque later and get her grams back.

The key is **256 bit** unsigned integer. Only hash of this key is stored in cheque smartcontract. Furthermore the key isn't sent to the blockchain while cheque creation.

# Files

- `generate-random-key.py`
  A python script to generate random 256 bit integer and print it in hex format. (There is no utilities in fift to generate random numbers, or I couldn't find it)

- `calculate-key-hash.fif` 
  An utility script to calculate SHA-256 of given 256 bit integer.

- `cheque-code.fc` 
  Code of cheque service smartcontract in FunC.

- `cheque-code.fc.fif`

  A compiled version of `cheque-code.fc`

- `create-cheque.fif`
  A script to create boc file containing information about future cheque: SHA256 of key and cheque value.

- `new-cheque-service.fif`
  A script for initializing new cheque service smartcontract

- `activate-cheque.fif`
  A script for creating external message to active cheque by key

# Usage

## Creating cheque

First of all you need to get key of future cheque. You can use any unsigned integer. There is a python script to generate random 256 bit unsigned integer:

`python generate-random-key.py`

It will print a random key in hex format. For example - 0x7.

The next step is to calculate SHA-256 hash. You can do it with a  help of script `calculate-key-hash.fif`

`fift -s calculate-key-hash.fif 0x7`

The output will be HEX representation of calculated hash. In our case:
`x{FEAB4032A52F46BD7110C6C8741F33EA0AFDAFAB4B0CB37F943B4F39963C29EE}`

**`FEAB4032A52F46BD7110C6C8741F33EA0AFDAFAB4B0CB37F943B4F39963C29EE`** is our hash

Then we need to create `boc` file containing data of our cheque:

`fift -s create-cheque.fif <KEY-HASH> <CHEQUE-VALUE> [<savefile>]`

`fift -s create-cheque.fif 0xFEAB4032A52F46BD7110C6C8741F33EA0AFDAFAB4B0CB37F943B4F39963C29EE 1` will create boc file `create-cheque-query.boc` representing cheque for 1 Gram.

And the last step is sending this grams from your wallet with attached generated boc file to cheque service smartcontract. 

**Fees for creating and activating cheque is around 0.15 GR so a cheque creator must send 0.15 GR more to the smartcontract**
In our case it will be 1.15 GR

## Activating cheque

So, we know a key of cheque. To activate it we need to send an external message to cheque service with our wallet address.

`fift -s activate-cheque.fif <CHEQUE-SERVICE-ADDRESS> <OUR-WALLET-ADDRESS> <SEQNO> <CHEQUE-KEY> [<SAVEFILE>]

After execution we will see `<SAVEFILE>.boc` (`create-cheque-query.boc`  by default)file. To finally activate cheque just send it via lite-client

**NOTE: Message sent from smartcontract to your wallet is non-bouncable, so you can use cheques for providing uninit wallet/smartcontracts with Grams **

## Creating your own cheque service

The process doesn't really differ from any default wallet creation:

`fift -s new-cheque-service.fif <WORKCHAIN> [<FILENAME-BASE>]` 

In the output you can see a non-bounceable address of your wallet. Provide it with some grams: send from another wallet or activate a cheque.

After that send created boc file(`cheque-service-query.boc` by default) via lite-client.

## Service methods

- `seqno`
  Returns current seqno of smartcontract
- `get-cheque-balance <KEY-HASH>`
  Checks wether cheque identified by given key exists. If it is than return its value in nanograms. Otherwise return -1

# Technical overwiew

The cheque is represented as pair `hash:uint256 -> slice(grams: Grams)` stored in dict in `c4`

Code of deployed contract cannot be upgraded.

More info you can get in `cheque-code.fc`

### Error codes

- 33 - invalid seqno

- 35 - invalid signature ( this error can appear only while initializing new cheque service)

  If you trying to create cheque and your message is bounced back it is because message value is lower than `CHEQUE-VALUE + 0.15` GR



# Possible improvements and issues

1. **Better fees handling**
   The smartcontract is supposed to be independent from balance replenishment. Fees for cheques processing must be provided by user who creates cheque. There is a need to calculate future fees more accurate. Now the constant value 0.15 GR is used because average total fees for cheque creation is around 0.06-0.075 GR. The same value is for cheque activation.
   The first step to handle this problem is using GASTOGRAM asm command. But now it is unsupported for some reasons.

   *I thought that fees will depend on number of cheques stored in c4, but there wasn't such behavior. Furthermore gas for cheque creation is not constant. This seems strange to me. But I can assume that the point is to check for the existence of a cheque with a given hash and it may take different gas to search for a specific key in dict*

2. **Cheque with multiple activation support**
   This feature can be very useful for some cases. There are some variants of implementation such chequeq:

   - Cheque value can be sent only once to specific address
   - Cheque can be activated only with given intervals

3. **Cheque expiration time support**

4. **Support for creating cheques that can accept/decline replenishment** 
   Now all cheques can be replenished.

5. **Support for cheques that will consume fees from the reciever, not the creator of cheque**
   This will require activation through internal message provided with fees and cheque key attached.

6. **~~If user sent more grams that intended, then return spare grams minus fees back~~ ** **DONE**

7. **Use bounceable messages on cheque activation**
   The real problem is handling bounced messages. First issue is fees handling if message bounced. And the second is recreating cheque when recieve bounced message.