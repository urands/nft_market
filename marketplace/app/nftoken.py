
from logging import getLogger
from shared import ton

import os

from tonclient.types import Abi, DeploySet, CallSet, Signer, FunctionHeader, \
    ParamsOfEncodeMessage, ParamsOfProcessMessage, ProcessingResponseType, \
    ProcessingEvent, ParamsOfSendMessage, ParamsOfWaitForTransaction, KeyPair,ParamsOfParse

from tonclient.types import ParamsOfConvertAddress, AddressStringFormat

log = getLogger('ton.py')


CONTRACT_DIR = ''


def call_from_root_function(func_name, params = {}):
    address_rtc = os.getenv('RTC_ADDRESS', '0:d9940684ab66b34e50f0e1062165ebd691c966430927fcafab519e3e11cf8942')
    signer_public = os.getenv('ROOT_SIGNER_PUBLIC', '')
    signer_secret = os.getenv('ROOT_SIGNER_SECRET', '')
    keypair = KeyPair(signer_public, signer_secret)
    signer = Signer.Keys(keys=keypair)
    call_set = CallSet(
        function_name=func_name,
        input = params,
    )
    events_abi = Abi.from_path(
            path=os.path.join(CONTRACT_DIR, 'RootTokenContract.abi.json'))

    encode_params = ParamsOfEncodeMessage(
            address = address_rtc,
            abi=events_abi,
            signer=signer, 
            call_set=call_set)

    process_params = ParamsOfProcessMessage(
                message_encode_params=encode_params, send_events=False)

    result = ton.processing.process_message(params=process_params)

    if result is None:
        raise ValueError('A very specific bad thing happened.')
        
    return result


def create_nf_token( pubkey, metadata  ):

    result = call_from_root_function('getTotalGranted', {})

    if (result):
        tokenId = int(result[0]) + 1

        result = call_from_root_function('getWalletAddress ', 
                    {   "workchain_id": 0,
                        "pubkey": pubkey})

        if (result):
            tokenAddress = result[0]

        result = call_from_root_function('mint',  {   "tokenId": tokenId  } )

        if (result or int(result[0]) != tokenId):
            raise ValueError('Mint error.')


        result = call_from_root_function('deployWallet', {
                "workchain_id": 0,
                "pubkey": pubkey,
                'tokenId': tokenId,
                'grams': 1            
        })

        if (result or int(result[0]) != tokenAddress):
            raise ValueError('Deploy error.')
        
        
        result = call_from_root_function('grant', {
                "dest": tokenAddress,
                'tokenId': tokenId,
                'grams': 1            
        })

        #log.info(f'create_nf_token {tokenId} {tokenAddress}')

        if (result):
            return (tokenId, tokenAddress)

        return None
