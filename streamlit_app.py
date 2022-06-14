import streamlit as st
import pandas as pd

USDC_MIN = 10


def main():
    print('START_MAIN')
    st.title("Arbitrum Airdrop Check")

    address = st.text_input('Enter Arbitrum address', placeholder='0x0f96...')
    # st.write(address)

    if address:
        # st.write('Address is', address)

        # data_load_state = st.text('Loading data...')
        result = search_address(address)
        # print(result)
        # data_load_state.text("Done! (using st.cache)")

        if result['status']:
            st.success('Eligible for Airdrop')
            st.write(result['data'])
            st.balloons()
        else:
            arbiscan_url = 'https://arbiscan.io/address/'
            arbiscan_url += address
            arbiscan_url += '#tokentxns'
            st.error(f'Not Eligible: {address}')
            st.write('Data', result['data'])

            if result['data'] and result['data']['usdc'] < USDC_MIN:
                st.warning(f'USDC balance is less than ${USDC_MIN}')
            if result['data'] and result['data']['is_contract']:
                st.warning(f'This is a contract address')

            st.write(f'Double check on Arbitrum Explorer ({arbiscan_url})')
            st.caption('Switch to “ERC20 Token Txns” and make a screenshot')

    print('END_MAIN')


@st.cache
def search_address(address):
    print('search_address', address)
    result = {
        'status': False,
        'data': None,
    }
    df = pd.read_csv("0607arbitrum-usdc-balance.csv")

    data = df.to_dict(orient='records')

    for row in data:
        if row['address'] == address:
            result['data'] = row
            if row['usdc'] >= USDC_MIN and row['is_contract'] is False:
                result['status'] = True

    return result


if __name__ == '__main__':
    main()
