define(['plugins/http', 'durandal/app', 'knockout'], function (http, app, ko) {
    return function () {
        var self = this;

        self.samples = ko.observable([]);

        var loadSamples = function () {
            return http.get('/api/v1.0/samples', {
            }).then(function (response) {
                self.samples(response.items);
            });
        };

        self.activate = function () {
            loadSamples();
        }
    };
});
