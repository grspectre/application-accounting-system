window.Util = {
    isUndefined: function(value) {
        return typeof value === 'undefined';
    },
    initDexie: function () {
        window.db = new Dexie("AppDatabase");
        window.db.version(1).stores({
            keyValue: '++id,key,value'
        })
    },
    checkAccessToken: async function () {
        let params = new URLSearchParams(document.location.search);
        let refreshToken = params.get('refresh_token');
        let accessToken = params.get('access_token');
        if (accessToken === null) {
            return;
        }
        let userToken = await window.db.keyValue.where({key: "user_token"}).first();
        let payload = {
            access_token: accessToken,
            refresh_token: refreshToken,
        };
        let obj = {
            key: 'user_token',
            value: JSON.stringify(payload),
        };

        if (this.isUndefined(userToken)) {
            await window.db.keyValue.put(obj);
        } else {
            await window.db.keyValue.put(obj, userToken.id);
        }

        params.delete('refresh_token');
        params.delete('access_token');

        let search = params.toString();
        if (search.length > 0) {
            search = '?'+search;
        } 
        document.location.search = params.toString();
    },
    setUserData: async function(payload) {
        let userData = await window.db.keyValue.where({key: "user_data"}).first();
        let obj = {
            key: 'user_data',
            value: JSON.stringify(payload),
        };

        if (this.isUndefined(userData)) {
            await window.db.keyValue.put(obj);
        } else {
            await window.db.keyValue.put(obj, userData.id);
        }
    },
    getAccessToken: async function() {
        let userToken = await window.db.keyValue.where({key: "user_token"}).first();
        if (!this.isUndefined(userToken)) {
            let data = JSON.parse(userToken.value);
            return 'Bearer '+data['access_token'];
        }
        return null;
    },
    getRequestParams: function(token) {
        return {
            headers: {
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        };
    },
    getAPIBaseUrl: function(action) {
        return document.location.origin+'/api/'+action;
    }
}

// main app initialization
document.addEventListener('alpine:init', () => {

    Util.initDexie();
    Util.checkAccessToken();

    Alpine.data('auth_block', () => ({
        baseUrl: '#',
        authorized: true,
        userData: null,
        dictionaries: [],
        orderList: null,
        async init() {
            let accessToken = await Util.getAccessToken();
            if (accessToken === null) { // we don't have access_token
                let url = 'https://pir.dfmb.ru/api/verify/yandex';
                let clientId = '0d90fed9dc3346b188a9d2e95c85a4cb'
                this.baseUrl = 'https://oauth.yandex.ru/authorize?response_type=code&redirect_uri=' + url + '&client_id=' + clientId;
                this.authorized = false;
            } else {
                let userData = await window.db.keyValue.where({key: "user_data"}).first();
                if (Util.isUndefined(userData)) {
                    await axios.get(Util.getAPIBaseUrl('user'), Util.getRequestParams(accessToken)).then(response => {
                        if (response.data.success) {
                            Util.setUserData(response.data.data);
                            this.userData = response.data.data;
                        }
                    });
                } else {
                    this.userData = JSON.parse(userData.value);
                }
            }

            // getting dictionaries
            axios.get(Util.getAPIBaseUrl('dictionary/all'), Util.getRequestParams(accessToken)).then(response => {
                if (response.data.success) {
                    this.dictionaries = response.data.dictionaries;
                }
            });
            this.getOrdersList();
        },

        async getOrdersList() {
            let accessToken = await Util.getAccessToken();
            axios.get(Util.getAPIBaseUrl('order/list'), Util.getRequestParams(accessToken)).then(response => {
                if (response.data.success) {
                   this.orderList = response.data.orders;
                }
            });
        },

        async createOrder() {
            let accessToken = await Util.getAccessToken();
            axios.post(Util.getAPIBaseUrl('order'), document.querySelector('#order-add'), Util.getRequestParams(accessToken)).then(response => {
                if (response.data.success) {
                   this.getOrdersList();
                }
            });
        },

        async logout() {
            await window.db.keyValue.where({key: "user_data"}).delete();
            await window.db.keyValue.where({key: "user_token"}).delete();
            document.location.reload();
        }
    }));
});

