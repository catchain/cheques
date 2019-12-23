# Description

This is a smart-contract for TON blockchain implementing wallet with multisend support made by CAT. It was made as a part of Telegram contest.

This wallet smartcontract can send multiple transactions with one external message. It can be useful for payments that must be sent to multiple users like regular payments to delegators.

# Files

- `multisend-code.fc` 
  Code of multisend wallet smartcontract in FunC.

- `multisend-code.fc.fif`

  A compiled version of `multisend-code.fc` 

- `multisend.fif`
  A script to create boc file containing several transactions to be sent


# Usage

## Creating your own multisend wallet

`fift -s new-multisend-wallet.fif <WORKCHAIN> [<FILENAME-BASE>]` 

In the output you can see a non-bounceable address of your wallet. Provide it with some grams: send from another wallet or activate a cheque.

After that send created boc file(`new-wallet-query.boc` by default) via lite-client.

## Sending grams

To send grams from multisend wallet you need to use `multisend.fif`

`fift -s multisend.fif  <wallet-filebase> <seqno> <savefile> <addr[1]> <amount[1]> [-B <attachment[1]] ... <addr[n]> <amount[n]> [-B <attachment[n]]`

Assume that you want to create some cheques and already created several boc files. You can do it this way:

`fift -s multisend.fif new-wallet 1 query kf8ihwLOYxUJecO7CNTyFoP5fDrZQw0NzQH9bN1kUZAxYaXc 1.15 -B create-cheque1-query.boc kf8ihwLOYxUJecO7CNTyFoP5fDrZQw0NzQH9bN1kUZAxYaXc 2.15 -B create-cheque2-query.boc kf8ihwLOYxUJecO7CNTyFoP5fDrZQw0NzQH9bN1kUZAxYaXc 10.15 -B create-cheque3-query.boc`

Then, send created `query.boc` file via lite-client.

## Smartcontract methods

- `seqno`
  Returns current seqno of smartcontract

## Fututure improvements

1. **Use stairs-like structure in external message to avoid using dicts and as a result, reduce fees even more**