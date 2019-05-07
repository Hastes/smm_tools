from vk_api import vk_api


def auth(token):
    vk_session = vk_api.VkApi(login='test', token=token)
    vk_session.auth(token_only=True)
    return vk_session.get_api()


def add_ads(token, name, description):
    vk = auth(token)
    data = {
        'name': name,
        'title': name,
        'link_url': 'https://hackathon.dissw.ru',
        'campaign_id': 1,
        "ad_format": 1,
        "cost_type": 0,
        "cpc": 2.00
    }
    result = vk.createAds(account_id=1604548878, data=[data])
    return None
