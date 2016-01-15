define(['modules/http', 'durandal/app', 'knockout'], function (http, app, ko) {
    return function () {
        var self = this;

        self.posts = ko.observable([]);

        var loadMyPostList = function () {
            return http.get('/api/v1.0/me/posts', {}).then(function (response) {
                self.posts(response.posts);
            });
        };

        self.activate = function () {
            loadMyPostList();
        }
    };
});
