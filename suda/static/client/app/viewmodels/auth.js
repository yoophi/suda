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
