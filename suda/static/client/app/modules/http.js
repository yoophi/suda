define(['jquery', 'knockout', 'plugins/http'], function ($, ko, http) {
    /**
     * @class HTTPModule
     * @static
     */
    var setHeaders = function(headers) {
        if (!headers)
            headers = {};
        var at = localStorage.getItem('access_token');
        if (at)
            headers['Authorization'] = 'bearer ' + at;
        return headers;
    };
    return {
        get: function (url, query, headers) {
            headers = setHeaders(headers);
            return http.get(url, query, headers);
        },
        post: function (url, query, headers) {
            headers = setHeaders(headers);
            return http.post(url, query, headers);
        }
    };
});
