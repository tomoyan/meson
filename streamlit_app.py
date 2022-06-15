import streamlit as st
import pandas as pd
from PIL import Image

USDC_MIN = 10


def main():
    print('START_MAIN')
    image = Image.open('favicon.ico')

    # app title and favicon settings
    st.set_page_config(
        page_title="Meson - Airdrop Check",
        page_icon=image,
    )

    st.title("Arbitrum Airdrop Check")
    st.subheader("Eligibility")
    st.write(
        "1. Successfully made at least one USDC transaction on Arbitrum\
        from 2022/5/1 at 00:00 GMT to 2022/6/7 at 23:59 GMT")
    st.write(
        "2. Holding 10 or more USDC balance on Arbitrum\
        at a snapshot time 2022/6/7 23:59 GMT")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "[Medium](https://medium.com/@mesonfi/cross-chain-airdrop-by-meson-on-arbitrum-9c5c783637a)",
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            "[Tutorial](https://legendary-judge-920.notion.site/Tutorial-How-to-check-an-address-in-Arbitrum-Airdrop-44c3a280f6464d2293b2a3f678efc882)",
            unsafe_allow_html=True)

    address = st.text_input('Enter Arbitrum address', placeholder='0x0f96...')
    address = address.strip()

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
    st.stop()


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
        if row['address'].lower() == address.lower():
            result['data'] = row
            if row['usdc'] >= USDC_MIN and row['is_contract'] is False:
                result['status'] = True
                break

    return result


if __name__ == '__main__':
    main()
