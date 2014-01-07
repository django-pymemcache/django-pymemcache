from pymemcache import client


class Client(client.Client):
    # this just fixes some API holes between python-memcached and pymemcache
    set_multi = client.Client.set_many
    get_multi = client.Client.get_many
    delete_multi = client.Client.delete_many
    disconnect_all = client.Client.quit
