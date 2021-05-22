# NTF Marketplace 

## Description
This repository is an attempt to create a MVP for working with NFT in freeton network with tokens of the TIP-3 standard. Initially, the tokens were taken from the official repository ["tonlabs/ton-labs-contracts"](https://github.com/tonlabs/ton-labs-contracts/tree/master/cpp/tokens-nonfungible).
Contracts deployed on test network: [net.ton.dev](net.ton.dev)

RootTokenContract : [0:d9940684ab66b34e50f0e1062165ebd691c966430927fcafab519e3e11cf8942](https://net.ton.live/accounts/accountDetails?id=0%3Ad9940684ab66b34e50f0e1062165ebd691c966430927fcafab519e3e11cf8942)

A token was deployed for account pubkey: 0x65eb078be1ae9186c4ff96e13e0cfe7f67e5cb388da72189260142cd49e4e069

TONTokenWallet: [0:fdd64bbb036d3f737779eef2ef8441abf4fa906bb282a1e89a6355c39d045bfc](https://net.ton.live/accounts/accountDetails?id=0%3Afdd64bbb036d3f737779eef2ef8441abf4fa906bb282a1e89a6355c39d045bfc)

These are test tokens and they do not have fields for storing meta information. Therefore, it was decided to expand their functionality. Also needed contract   to buy/sell transactions of tokens.
![img](./docs/token.png)



## Requirements

- Install [Docker](https://www.docker.com/products/docker-desktop)
- `git clone https://github.com/urands/nft_market.git`

## Instalation/run

```bash
docker-compose build
docker-compose up -d
```
