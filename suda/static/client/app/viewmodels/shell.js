define(['plugins/router', 'durandal/app'], function (router, app) {
    return {
        router: router,
        search: function () {
            //It's really easy to show a message box.
            //You can add custom options too. Also, it returns a promise for the user's response.
            app.showMessage('Search not yet implemented...');
        },
        activate: function () {
            router.map([
                {
                    route: 'auth',
                    title: 'Auth',
                    moduleId: 'viewmodels/auth',
                    nav: true
                },
                {
                    route: 'my_post_list',
                    title: 'My Posts',
                    moduleId: 'viewmodels/my_post_list',
                    nav: true
                },
                {
                    route: '',
                    title: 'Suda',
                    moduleId: 'viewmodels/suda',
                    nav: true
                },
            ]).buildNavigationModel();

            return router.activate();
        }
    };
});