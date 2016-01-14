define(['plugins/http', 'knockout'], function (http, ko) {
    $(document).ajaxError(function (e, event) {
        if (event.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.hash = '#auth';
        }
    });

    return function () {
        var self = this;

        self.data = ko.observable('');
        self.isLogged = ko.observable(false);
        self.hasPhoneCertRequestResut = ko.observable(false);
        self.triedAuthentication = ko.observable(false);
        self.cert_key = ko.observable('')
        self.phone_no = ko.observable('')
        self.response = {
            auth: ko.observable(''),
            me: ko.observable(''),
            cert_key: ko.observable('')
        };

        var authenticate = function (username, password) {
            var data = {
                grant_type: "password",
                client_id: "foo",
                client_secret: "secret",
                username: username,
                password: password,
                scope: "email"
            };
            self.data(JSON.stringify(data));
            return $.ajax({
                url: '/api/v1.0/oauth/token',
                type: 'post',
                data: data
            });
        };

        var call_me = function (access_token) {
            return http.get('/api/v1.0/me', {}, {
                'Authorization': 'bearer ' + access_token
            })
        };

        var phone_cert_request = function(phone_no) {
            self.phone_no(phone_no)
            var data = {
                phone_no: phone_no
            };

            self.data(JSON.stringify(data))
            var at = localStorage.getItem('access_token')
            return http.post('/api/v1.0/me/phone_cert/request', data, {
                'Authorization': 'bearer ' + at
            }).then(function(response) {
                self.hasPhoneCertRequestResut(true)
                self.cert_key(response.cert_key)
                self.response.cert_key(JSON.stringify(response))
            })
        }

        var phone_cert_verify = function(phone_no, cert_key, cert_code) {
            var data = {
                cert_key: cert_key,
                cert_code: cert_code,
                phone_no: phone_no,
            };

            self.data(JSON.stringify(data))
            var at = localStorage.getItem('access_token')
            return http.post('/api/v1.0/me/phone_cert/submit', data, {
                'Authorization': 'bearer ' + at
            }).then(function(response) {
                var at = localStorage.getItem('access_token')
                call_me(at).then(function (response) {
                    self.response.me(JSON.stringify(response));
                });
            })
        }

        var update_extra = function(nickname, address) {
            var data = {
                nickname: nickname,
                address: address
            }

            var at = localStorage.getItem('access_token')
            return http.post('/api/v1.0/me/extra_info', data, {
                'Authorization': 'bearer ' + at
            }).then(function(response) {
                if (response.result == 'ok') {
                    alert('반영되었습니다')
                }

                var at = localStorage.getItem('access_token')
                call_me(at).then(function (response) {
                    self.response.me(JSON.stringify(response));
                });
            })

        }
        self.tryAuthenticate = function (form) {
            self.triedAuthentication(true)

            if (form.username.value.trim() == '')
                return false;
            if (form.password.value == '')
                return false;
            return authenticate(form.username.value.trim(), form.password.value).then(function (response) {
                localStorage.setItem('access_token', response.access_token)
                localStorage.setItem('refresh_token', response.refresh_token)
                self.response.auth(JSON.stringify(response));
                self.isLogged(true);

                return call_me(response.access_token).then(function (response) {
                    self.response.me(JSON.stringify(response));
                });
            })
        };

        self.tryPhoneCert = function(form) {
            if (form.phone_no.value.trim() == '')
                return false

            return phone_cert_request(form.phone_no.value.trim())
        }

        self.tryPhoneCertVerify =  function(form) {
            if (form.cert_code.value.trim() == '')
                return false

            return phone_cert_verify(form.phone_no.value.trim(), form.cert_key.value.trim(), form.cert_code.value.trim())
        }

        self.tryUpdateExtra = function(form) {
            ref1 = ['nickname', 'address'];
            for (k = 0, len1 = ref1.length; k < len1; k++) {
                key = ref1[k];
                if (form[key].value.trim() === '') {
                    return false;
                }
            }

            return update_extra(form.nickname.value.trim(), form.address.value.trim())
        }


        self.logout = function () {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            self.isLogged(false);
        };

        self.activate = function () {
            var at = localStorage.getItem('access_token')
            if (at) {
                self.isLogged(true)
                return call_me(at).then(function (response) {
                    self.response.me(JSON.stringify(response));
                });
            }
        }
    };
});
